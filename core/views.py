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
    """Generate SEO-optimized robots.txt"""
    lines = [
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin and private areas",
        "Disallow: /admin/",
        "Disallow: /account/login/",
        "Disallow: /account/register/",
        "Disallow: /account/password-reset/",
        "",
        "# Disallow media uploads directory",
        "Disallow: /media/",
        "",
        "# Sitemap location",
        f"Sitemap: {request.build_absolute_uri(reverse('sitemap_xml'))}",
        "",
        "# Crawl delay",
        "Crawl-delay: 1",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    """Generate SEO-optimized XML sitemap with lastmod and priority"""
    
    # Helper function to generate URL entries
    def make_url_entry(url, lastmod=None, priority="0.8", changefreq="weekly"):
        entry = f"  <url>\n    <loc>{url}</loc>"
        if lastmod:
            entry += f"\n    <lastmod>{lastmod.isoformat()}</lastmod>"
        entry += f"\n    <changefreq>{changefreq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        return entry
    
    urls = []
    
    # Home page - highest priority
    home_url = request.build_absolute_uri(reverse("home"))
    urls.append(make_url_entry(home_url, priority="1.0", changefreq="daily"))
    
    # Shop page
    shop_url = request.build_absolute_uri(reverse("products:shop"))
    urls.append(make_url_entry(shop_url, priority="0.9", changefreq="daily"))
    
    # Categories page
    categories_url = request.build_absolute_uri(reverse("categories:list"))
    urls.append(make_url_entry(categories_url, priority="0.8", changefreq="weekly"))
    
    # Individual categories
    for category in Category.objects.filter(is_active=True):
        cat_url = request.build_absolute_uri(category.get_absolute_url())
        urls.append(make_url_entry(cat_url, None, priority="0.8", changefreq="weekly"))
    
    # Individual products
    for product in Product.objects.active():
        prod_url = request.build_absolute_uri(product.get_absolute_url())
        urls.append(make_url_entry(prod_url, product.updated_at, priority="0.7", changefreq="monthly"))
    
    # Active campaigns
    for campaign in Campaign.objects.filter(is_active=True):
        camp_url = request.build_absolute_uri(campaign.get_absolute_url())
        urls.append(make_url_entry(camp_url, campaign.created_at, priority="0.6", changefreq="weekly"))
    
    body = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        "\n".join(urls),
        "</urlset>"
    ]
    return HttpResponse("\n".join(body), content_type="application/xml")
