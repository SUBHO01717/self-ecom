from django.urls import path

from . import views

app_name = "customers"

urlpatterns = [
    path("login/", views.customer_login, name="login"),
    path("logout/", views.customer_logout, name="logout"),
    path("activate-account/", views.activate_account, name="activate_account"),
    path("", views.dashboard, name="dashboard"),
]
