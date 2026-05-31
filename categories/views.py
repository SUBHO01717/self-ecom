from django.shortcuts import get_object_or_404, render

from products.models import Product
from .models import Category


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "categories/category_list.html", {"categories": categories, "page_title": "Categories"})


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.active().filter(category=category)
    return render(request, "categories/category_products.html", {"category": category, "products": products, "seo_object": category})
