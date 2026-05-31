from decimal import Decimal
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from campaigns.models import Campaign
from categories.models import Category
from customers.models import CustomerProfile
from orders.models import Order, OrderItem, PromoCode
from products.models import Color, Product, ProductImage, Size
from settings_manager.models import Banner, OfferStrip, SiteSettings


class Command(BaseCommand):
    help = "Populate Daily Essentials with reusable dummy data."

    def handle(self, *args, **options):
        image_paths = self._ensure_seed_images()
        settings_obj = self._seed_settings()
        banners = self._seed_banners(image_paths)
        offers = self._seed_offers()
        categories = self._seed_categories(image_paths)
        sizes = self._seed_sizes()
        colors = self._seed_colors()
        products = self._seed_products(categories, sizes, colors, image_paths)
        gallery = self._seed_product_images(products, image_paths)
        campaigns = self._seed_campaigns(products, image_paths)
        promos = self._seed_promos()
        customers = self._seed_customers()
        orders, items = self._seed_orders(customers, products)

        self.stdout.write(self.style.SUCCESS("Dummy data ready."))
        self.stdout.write(
            "Created/available counts: "
            f"settings=1, banners={len(banners)}, offers={len(offers)}, "
            f"categories={len(categories)}, sizes={len(sizes)}, colors={len(colors)}, "
            f"products={len(products)}, product_images={len(gallery)}, "
            f"campaigns={len(campaigns)}, promos={len(promos)}, customers={len(customers)}, "
            f"orders={len(orders)}, order_items={len(items)}"
        )
        self.stdout.write(f"Site settings record: {settings_obj}")

    def _ensure_seed_images(self):
        from PIL import Image, ImageDraw

        seed_dir = Path(settings.MEDIA_ROOT) / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)
        palette = [
            ("#047857", "#d1fae5"),
            ("#0f172a", "#e2e8f0"),
            ("#be123c", "#ffe4e6"),
            ("#1d4ed8", "#dbeafe"),
            ("#a16207", "#fef3c7"),
            ("#7c3aed", "#ede9fe"),
            ("#0f766e", "#ccfbf1"),
            ("#c2410c", "#ffedd5"),
            ("#4338ca", "#e0e7ff"),
            ("#15803d", "#dcfce7"),
        ]
        paths = []
        for index, (primary, background) in enumerate(palette, start=1):
            path = seed_dir / f"dummy-{index}.jpg"
            if not path.exists():
                image = Image.new("RGB", (1200, 800), background)
                draw = ImageDraw.Draw(image)
                draw.rectangle((80, 80, 1120, 720), outline=primary, width=18)
                draw.rectangle((140, 520, 1060, 650), fill=primary)
                draw.text((180, 560), f"Daily Essentials {index}", fill="#ffffff")
                image.save(path, "JPEG", quality=90)
            paths.append(f"seed/{path.name}")
        return paths

    def _seed_settings(self):
        settings_obj = SiteSettings.load()
        settings_obj.site_name = settings_obj.site_name or "Daily Essentials"
        settings_obj.seo_title = settings_obj.seo_title or "Daily Essentials - Online Shop"
        settings_obj.meta_description = settings_obj.meta_description or "Shop fresh and useful daily essentials online."
        settings_obj.meta_keywords = settings_obj.meta_keywords or "daily essentials, ecommerce, groceries, household"
        settings_obj.whatsapp_number = settings_obj.whatsapp_number or "8801700000000"
        settings_obj.save()
        return settings_obj

    def _seed_banners(self, image_paths):
        banners = []
        for index in range(1, 11):
            banner, _created = Banner.objects.get_or_create(
                title=f"Fresh Essentials Deal {index}",
                defaults={
                    "subtitle": f"Save more on everyday picks batch {index}.",
                    "button_text": "Shop Now",
                    "button_url": "/shop/",
                    "background_image": image_paths[(index - 1) % len(image_paths)],
                    "is_active": True,
                    "display_order": index,
                },
            )
            banners.append(banner)
        return banners

    def _seed_offers(self):
        offers = []
        texts = [
            "Free Delivery Over ৳1000",
            "10% Discount on First Order",
            "Fresh Deals Every Morning",
            "Cash on Delivery Available",
            "bKash Manual Payment Supported",
            "Nagad Manual Payment Supported",
            "Weekend Household Sale",
            "Bundle Offers on Groceries",
            "Fast Delivery in Dhaka",
            "New Arrivals Added Weekly",
        ]
        for index, text in enumerate(texts, start=1):
            offer, _created = OfferStrip.objects.get_or_create(text=text, defaults={"is_active": True, "display_order": index})
            offers.append(offer)
        return offers

    def _seed_categories(self, image_paths):
        names = ["Groceries", "Personal Care", "Home Cleaning", "Baby Care", "Snacks", "Beverages", "Kitchen", "Health", "Beauty", "Pet Supplies"]
        categories = []
        for index, name in enumerate(names, start=1):
            category, _created = Category.objects.get_or_create(
                slug=slugify(name),
                defaults={
                    "name": name,
                    "image": image_paths[(index - 1) % len(image_paths)],
                    "description": f"Useful {name.lower()} products for everyday shopping.",
                    "is_active": True,
                    "show_on_home": index <= 6,
                    "display_order": index,
                    "seo_title": f"{name} | Daily Essentials",
                    "meta_description": f"Shop {name.lower()} online at Daily Essentials.",
                },
            )
            categories.append(category)
        return categories

    def _seed_sizes(self):
        names = ["One Size", "Small", "Medium", "Large", "Extra Large", "Double Extra Large", "250 ml", "500 ml", "1 kg", "5 kg"]
        sizes = []
        for index, name in enumerate(names, start=1):
            size, _created = Size.objects.get_or_create(name=name, defaults={"display_order": index})
            sizes.append(size)
        return sizes

    def _seed_colors(self):
        values = [
            ("Red", "#ef4444"),
            ("Green", "#22c55e"),
            ("Blue", "#3b82f6"),
            ("Black", "#111827"),
            ("White", "#ffffff"),
            ("Yellow", "#eab308"),
            ("Pink", "#ec4899"),
            ("Purple", "#8b5cf6"),
            ("Brown", "#92400e"),
            ("Grey", "#64748b"),
        ]
        colors = []
        for name, hex_code in values:
            color, _created = Color.objects.get_or_create(name=name, defaults={"hex_code": hex_code})
            colors.append(color)
        return colors

    def _seed_products(self, categories, sizes, colors, image_paths):
        products = []
        for index in range(1, 11):
            category = categories[(index - 1) % len(categories)]
            price = Decimal("150.00") + Decimal(index * 75)
            discount_price = price - Decimal("25.00") if index % 2 == 0 else None
            product, _created = Product.objects.get_or_create(
                slug=f"dummy-product-{index}",
                defaults={
                    "category": category,
                    "name": f"Dummy Product {index}",
                    "short_description": f"A practical daily essential product number {index}.",
                    "full_description": f"Dummy Product {index} is created for testing product detail pages, cart flow, filters, labels, SEO, and admin management.",
                    "sku": f"DUMMY-{index:03d}",
                    "price": price,
                    "discount_price": discount_price,
                    "stock_quantity": 20 + index,
                    "thumbnail": image_paths[(index - 1) % len(image_paths)],
                    "size_guide": image_paths[index % len(image_paths)],
                    "is_active": True,
                    "is_featured": index <= 5,
                    "is_new_arrival": index in {1, 2, 3, 6, 7},
                    "is_bestseller": index in {2, 4, 6, 8, 10},
                    "is_campaign_product": index >= 6,
                    "seo_title": f"Dummy Product {index} | Daily Essentials",
                    "meta_description": f"Buy Dummy Product {index} online from Daily Essentials.",
                },
            )
            product.sizes.set(sizes[max(0, index - 3) : index] or sizes[:3])
            product.colors.set(colors[max(0, index - 3) : index] or colors[:3])
            products.append(product)
        return products

    def _seed_product_images(self, products, image_paths):
        images = []
        for index, product in enumerate(products, start=1):
            image, _created = ProductImage.objects.get_or_create(
                product=product,
                display_order=1,
                defaults={
                    "image": image_paths[index % len(image_paths)],
                    "alt_text": f"{product.name} gallery image",
                },
            )
            images.append(image)
        return images

    def _seed_campaigns(self, products, image_paths):
        campaigns = []
        for index in range(1, 11):
            campaign, _created = Campaign.objects.get_or_create(
                slug=f"dummy-campaign-{index}",
                defaults={
                    "title": f"Dummy Campaign {index}",
                    "banner_image": image_paths[(index - 1) % len(image_paths)],
                    "offer_text": f"Special campaign offer {index}",
                    "discount_percentage": min(70, index * 5),
                    "is_active": True,
                    "seo_title": f"Dummy Campaign {index} | Daily Essentials",
                    "meta_description": f"Explore campaign products for Dummy Campaign {index}.",
                },
            )
            campaign.products.set(products[max(0, index - 3) : index] or products[:3])
            campaigns.append(campaign)
        return campaigns

    def _seed_promos(self):
        promos = []
        for index in range(1, 11):
            promo, _created = PromoCode.objects.get_or_create(
                code=f"SAVE{index * 5}",
                defaults={
                    "description": f"Dummy promo code {index}",
                    "discount_type": PromoCode.DiscountType.PERCENT if index % 2 else PromoCode.DiscountType.FIXED,
                    "discount_value": Decimal(index * 5 if index % 2 else index * 20),
                    "minimum_order_amount": Decimal("100.00"),
                    "maximum_discount_amount": Decimal("500.00") if index % 2 else None,
                    "is_active": True,
                    "usage_limit": 100,
                },
            )
            promos.append(promo)
        return promos

    def _seed_customers(self):
        User = get_user_model()
        customers = []
        for index in range(1, 11):
            email = f"customer{index}@example.com"
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    "email": email,
                    "first_name": f"Customer {index}",
                },
            )
            if created:
                user.set_password("Customer12345")
                user.save()
            profile, _created = CustomerProfile.objects.get_or_create(
                user=user,
                defaults={
                    "phone": f"017000000{index:02d}",
                    "shipping_address": f"House {index}, Road {index}, Dhaka",
                },
            )
            customers.append(profile)
        return customers

    def _seed_orders(self, customers, products):
        orders = []
        items = []
        statuses = [choice[0] for choice in Order.Status.choices]
        methods = [choice[0] for choice in Order.PaymentMethod.choices]
        for index, profile in enumerate(customers, start=1):
            product = products[(index - 1) % len(products)]
            quantity = 1 + (index % 3)
            subtotal = product.current_price * quantity
            order, _created = Order.objects.get_or_create(
                phone=profile.phone,
                full_name=profile.user.get_full_name() or profile.user.username,
                defaults={
                    "customer": profile.user,
                    "email": profile.user.email,
                    "shipping_address": profile.shipping_address,
                    "status": statuses[(index - 1) % len(statuses)],
                    "payment_method": methods[(index - 1) % len(methods)],
                    "transaction_id": f"TXN{index:06d}" if methods[(index - 1) % len(methods)] != Order.PaymentMethod.COD else "",
                    "payment_verified": index % 2 == 0,
                    "subtotal": subtotal,
                    "purchase_pixel_pending": statuses[(index - 1) % len(statuses)] == Order.Status.COMPLETED,
                },
            )
            item, _created = OrderItem.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    "product_name": product.name,
                    "sku": product.sku,
                    "quantity": quantity,
                    "price": product.current_price,
                },
            )
            orders.append(order)
            items.append(item)
        return orders, items
