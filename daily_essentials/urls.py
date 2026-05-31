from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from core.views import home, robots_txt, sitemap_xml

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("categories/", include("categories.urls")),
    path("shop/", include("products.urls")),
    path("campaigns/", include("campaigns.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("account/", include("customers.urls")),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap_xml, name="sitemap_xml"),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
