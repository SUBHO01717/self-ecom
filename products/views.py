from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from categories.models import Category
from .models import Product


def shop(request):
    products = Product.objects.active()
    categories = Category.objects.filter(is_active=True)
    category_slug = request.GET.get("category")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort", "newest")

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if request.GET.get("in_stock"):
        products = products.filter(stock_quantity__gt=0)
    for key, field in {
        "featured": "is_featured",
        "new": "is_new_arrival",
        "bestseller": "is_bestseller",
        "campaign": "is_campaign_product",
    }.items():
        if request.GET.get(key):
            products = products.filter(**{field: True})
    products = products.order_by("created_at" if sort == "oldest" else "-created_at")
    return render(request, "products/shop.html", {"products": products, "categories": categories, "page_title": "Shop"})


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.active().prefetch_related("sizes", "colors", "gallery"), slug=slug)
    related = Product.objects.active().filter(category=product.category).exclude(pk=product.pk)[:4]
    return render(request, "products/product_detail.html", {"product": product, "related_products": related, "seo_object": product})
