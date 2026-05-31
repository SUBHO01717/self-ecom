from django.shortcuts import get_object_or_404, render

from .models import Campaign


def campaign_list(request):
    campaigns = Campaign.objects.filter(is_active=True).prefetch_related("products")
    return render(request, "campaigns/campaign_list.html", {"campaigns": campaigns, "page_title": "Campaigns"})


def campaign_detail(request, slug):
    campaign = get_object_or_404(Campaign.objects.prefetch_related("products"), slug=slug, is_active=True)
    return render(request, "campaigns/campaign_detail.html", {"campaign": campaign, "products": campaign.products.active(), "seo_object": campaign})
