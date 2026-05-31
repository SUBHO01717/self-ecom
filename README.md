# Daily Essentials

Dynamic Django e-commerce website using function-based views, Django Admin content management, Tailwind CSS, SQLite, and a session cart.

## Features

- Admin-managed banners, offer strips, categories, products, product images, variants, campaigns, SEO, tracking scripts, social links, email toggle, customers, and orders.
- Homepage with hero slider, offer strip, top categories, new arrival, featured, and bestseller product sections.
- Shop page with category, price, sort, stock, featured, new arrival, bestseller, and campaign filters.
- Guest checkout with automatic customer account creation.
- COD, bKash manual payment, and Nagad manual payment support.
- Facebook Pixel `Purchase` event is deferred until an admin marks an order `Completed`; the customer-facing order page then fires the event once and records it as fired.
- SEO fields, clean slug URLs, `robots.txt`, `sitemap.xml`, Open Graph metadata, and product schema basics.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The bundled runtime used during development in this workspace is:

```powershell
C:\Users\SUBHO\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe manage.py runserver
```

## Admin Notes

Open `/admin/` to manage all site content. Email is disabled by default in `SiteSettings`. Add Facebook Pixel ID, Google Analytics ID, custom scripts, social URLs, WhatsApp number, and homepage SEO from the singleton Site Settings record.
