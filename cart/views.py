from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Color, Product, Size
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart, "page_title": "Cart"})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product.objects.active().prefetch_related("sizes", "colors"), id=product_id)
    if product.stock_quantity <= 0:
        messages.error(request, f"{product.name} is currently out of stock.")
        return redirect(request.POST.get("next") or product.get_absolute_url())

    selected_size = None
    selected_color = None
    size_id = request.POST.get("size")
    color_id = request.POST.get("color")
    if product.sizes.exists():
        selected_size = product.sizes.filter(id=size_id).first()
        if selected_size is None:
            messages.error(request, "Please select a size before adding this product to cart.")
            return redirect(product.get_absolute_url())
    if product.colors.exists():
        selected_color = product.colors.filter(id=color_id).first()
        if selected_color is None:
            messages.error(request, "Please select a color before adding this product to cart.")
            return redirect(product.get_absolute_url())

    Cart(request).add(product, request.POST.get("quantity", 1), size=selected_size, color=selected_color)
    messages.success(request, f"{product.name} added to cart.")
    return redirect(request.POST.get("next") or "cart:detail")


def update_cart(request, item_key):
    Cart(request).update(item_key, request.POST.get("quantity", 1))
    return redirect("cart:detail")


def remove_from_cart(request, item_key):
    Cart(request).remove(item_key)
    return redirect("cart:detail")
