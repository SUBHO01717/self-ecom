from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render


from cart.cart import Cart
from customers.models import CustomerProfile
from settings_manager.models import SiteSettings, ShippingArea
from .forms import CheckoutForm
from .models import Order, OrderItem, PromoCode


def _get_or_create_customer(order):
    User = get_user_model()

    username = order.email or order.phone

    # Check existing customer by username, email or phone
    user = (
        User.objects.filter(username=username).first()
        or User.objects.filter(email__iexact=order.email).first()
        or User.objects.filter(customer_profile__phone=order.phone).first()
    )

    created = False

    if user is None:
        created = True

        user = User.objects.create_user(
            username=username,
            email=order.email,
            first_name=order.full_name,
        )

        # Customer must set password later
        user.set_unusable_password()
        user.save()

    profile, _ = CustomerProfile.objects.get_or_create(user=user)

    profile.phone = order.phone
    profile.shipping_address = order.shipping_address
    profile.save()

    return user, created

def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:detail")

    subtotal = cart.total()
    promo = None
    discount_amount = 0
    promo_code = cart.promo_code()
    if promo_code:
        promo = PromoCode.objects.filter(code__iexact=promo_code).first()
        if promo:
            is_valid, error = promo.is_valid_for_subtotal(subtotal)
            if is_valid:
                discount_amount = promo.calculate_discount(subtotal)
            else:
                messages.error(request, error)
                cart.remove_promo_code()
                promo = None
        else:
            messages.error(request, "Invalid promo code.")
            cart.remove_promo_code()

    # Determine shipping cost from selected area
    shipping_areas = ShippingArea.objects.filter(is_active=True)
    shipping_cost = 0
    selected_area_id = request.POST.get("shipping_area") or request.session.get("selected_shipping_area_id")
    selected_area = None
    if selected_area_id:
        try:
            selected_area = ShippingArea.objects.get(pk=selected_area_id, is_active=True)
            shipping_cost = selected_area.courier_fee
            request.session["selected_shipping_area_id"] = selected_area.pk
        except ShippingArea.DoesNotExist:
            selected_area = None
            shipping_cost = 0

    total = subtotal - discount_amount + shipping_cost

    if request.method == "POST" and request.POST.get("promo_action") == "apply":
        code = request.POST.get("promo_code", "").strip()
        if not code:
            messages.error(request, "Please enter a promo code.")
        else:
            promo = PromoCode.objects.filter(code__iexact=code).first()
            if promo is None:
                messages.error(request, "Invalid promo code.")
            else:
                is_valid, error = promo.is_valid_for_subtotal(subtotal)
                if is_valid:
                    cart.set_promo_code(promo.code)
                    messages.success(request, f"Promo code {promo.code} applied.")
                else:
                    messages.error(request, error)
        return redirect("orders:checkout")

    if request.method == "POST" and request.POST.get("promo_action") == "remove":
        cart.remove_promo_code()
        messages.success(request, "Promo code removed.")
        return redirect("orders:checkout")

    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        if promo_code and promo is None:
            messages.error(request, "Please apply a valid promo code or remove it before placing the order.")
            return redirect("orders:checkout")
        with transaction.atomic():
            order = form.save(commit=False)
            order.subtotal = subtotal
            order.promo_code = promo.code if promo else ""
            order.discount_amount = discount_amount
            order.shipping_area = selected_area
            order.shipping_cost = shipping_cost
            order.total = total
            user, created = _get_or_create_customer(order)
            order.customer = user
            order.save()
            for item in cart:
                product = item["product"]
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    sku=product.sku,
                    selected_size=item.get("size_name", ""),
                    selected_color=item.get("color_name", ""),
                    quantity=item["quantity"],
                    price=product.current_price,
                )
                product.stock_quantity = max(0, product.stock_quantity - item["quantity"])
                product.save(update_fields=["stock_quantity"])
            if promo:
                PromoCode.objects.filter(pk=promo.pk).update(used_count=promo.used_count + 1)
            if SiteSettings.load().email_enabled and order.email:
                send_mail("Your Daily Essentials order", f"Thanks for your order #{order.pk}. Status: Pending.", None, [order.email], fail_silently=True)
            cart.clear()
            request.session.pop("selected_shipping_area_id", None)
            login(request, user)
            if created:
                messages.info(
                    request,
                    "An account has been created for you. To access it later, use your email or phone number and click 'Set Password' on the login page."
                )
        messages.success(request, "Order placed successfully. Your order is pending confirmation.")
        return redirect("orders:detail", order.pk)
    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart": cart,
            "page_title": "Checkout",
            "applied_promo": promo,
            "promo_code": promo_code,
            "discount_amount": discount_amount,
            "checkout_subtotal": subtotal,
            "checkout_total": total,
            "shipping_areas": shipping_areas,
            "shipping_cost": shipping_cost,
            "selected_area": selected_area,
        },
    )


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id, customer=request.user)
    should_fire_purchase = order.status == Order.Status.COMPLETED and order.purchase_pixel_pending and not order.purchase_pixel_fired
    return render(request, "orders/order_detail.html", {"order": order, "should_fire_purchase": should_fire_purchase, "page_title": f"Order #{order.pk}"})


@login_required
def mark_purchase_pixel_fired(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    if request.method == "POST" and order.status == Order.Status.COMPLETED:
        order.purchase_pixel_pending = False
        order.purchase_pixel_fired = True
        order.save(update_fields=["purchase_pixel_pending", "purchase_pixel_fired"])
    return JsonResponse({"ok": True})
