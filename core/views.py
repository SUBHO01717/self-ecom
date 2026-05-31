from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse

from campaigns.models import Campaign
from categories.models import Category
from products.models import Product
from settings_manager.models import Banner, OfferStrip, SiteSettings


def home(request):
    settings = SiteSettings.load()
    context = {
        "seo_object": settings,
        "banners": Banner.objects.filter(is_active=True).order_by("display_order"),
        "offers": OfferStrip.objects.filter(is_active=True).order_by("display_order"),
        "top_categories": Category.objects.filter(is_active=True, show_on_home=True).order_by("display_order", "name")[:6],
        "new_arrivals": Product.objects.active().filter(is_new_arrival=True)[:8],
        "featured_products": Product.objects.active().filter(is_featured=True)[:8],
        "best_sellers": Product.objects.active().filter(is_bestseller=True)[:8],
    }
    return render(request, "core/home.html", context)


def robots_txt(request):
    lines = ["User-agent: *", "Allow: /", f"Sitemap: {request.build_absolute_uri(reverse('sitemap_xml'))}"]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    urls = [request.build_absolute_uri(reverse("home")), request.build_absolute_uri(reverse("products:shop")), request.build_absolute_uri(reverse("categories:list"))]
    urls += [request.build_absolute_uri(category.get_absolute_url()) for category in Category.objects.filter(is_active=True)]
    urls += [request.build_absolute_uri(product.get_absolute_url()) for product in Product.objects.active()]
    urls += [request.build_absolute_uri(campaign.get_absolute_url()) for campaign in Campaign.objects.filter(is_active=True)]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    body += [f"<url><loc>{url}</loc></url>" for url in urls]
    body.append("</urlset>")
    return HttpResponse("\n".join(body), content_type="application/xml")
