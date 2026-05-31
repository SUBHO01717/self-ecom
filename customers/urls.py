from django.urls import path

from . import views

app_name = "customers"

urlpatterns = [
    path("login/", views.customer_login, name="login"),
    path("logout/", views.customer_logout, name="logout"),
    path("", views.dashboard, name="dashboard"),
]
