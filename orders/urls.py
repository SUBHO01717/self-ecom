from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("<int:order_id>/", views.order_detail, name="detail"),
    path("<int:order_id>/pixel-fired/", views.mark_purchase_pixel_fired, name="pixel_fired"),
]
