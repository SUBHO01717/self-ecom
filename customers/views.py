from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from orders.models import Order
from .forms import CustomerLoginForm


def customer_login(request):
    form = CustomerLoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.cleaned_data["user"])
        return redirect("customers:dashboard")
    return render(request, "customers/login.html", {"form": form, "page_title": "Login"})


def customer_logout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    orders = Order.objects.filter(customer=request.user).prefetch_related("items").order_by("-created_at")
    completed_orders_count = orders.filter(status=Order.Status.COMPLETED).count()
    return render(request, "customers/dashboard.html", {
        "orders": orders,
        "completed_orders_count": completed_orders_count,
        "page_title": "Dashboard"
    })
