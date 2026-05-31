from decimal import Decimal

from products.models import Product


class Cart:
    session_key = "cart"
    promo_session_key = "promo_code"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(self.session_key, {})

    def _item_key(self, product_id, size_id="", color_id=""):
        return f"{product_id}:{size_id or ''}:{color_id or ''}"

    def add(self, product, quantity=1, size=None, color=None):
        item_key = self._item_key(product.id, getattr(size, "id", ""), getattr(color, "id", ""))
        item = self.cart.setdefault(
            item_key,
            {
                "product_id": product.id,
                "quantity": 0,
                "size_id": getattr(size, "id", None),
                "size_name": getattr(size, "name", ""),
                "color_id": getattr(color, "id", None),
                "color_name": getattr(color, "name", ""),
            },
        )
        item["quantity"] = min(product.stock_quantity, item["quantity"] + int(quantity))
        self.save()

    def update(self, item_key, quantity):
        item_key = str(item_key)
        if item_key in self.cart:
            quantity = int(quantity)
            if quantity <= 0:
                self.remove(item_key)
            else:
                self.cart[item_key]["quantity"] = quantity
                self.save()

    def remove(self, item_key):
        self.cart.pop(str(item_key), None)
        self.save()

    def clear(self):
        self.session[self.session_key] = {}
        self.session.pop(self.promo_session_key, None)
        self.session.modified = True

    def save(self):
        self.session[self.session_key] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = [item.get("product_id", key.split(":")[0]) for key, item in self.cart.items()]
        products = Product.objects.filter(id__in=product_ids)
        product_map = {str(product.id): product for product in products}
        for item_key, item in self.cart.items():
            product_id = str(item.get("product_id", item_key.split(":")[0]))
            product = product_map.get(product_id)
            if not product:
                continue
            quantity = item["quantity"]
            yield {
                "key": item_key,
                "product": product,
                "quantity": quantity,
                "size_name": item.get("size_name", ""),
                "color_name": item.get("color_name", ""),
                "line_total": product.current_price * quantity,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def total(self):
        return sum((item["line_total"] for item in self), Decimal("0.00"))

    def set_promo_code(self, code):
        self.session[self.promo_session_key] = code.upper().strip()
        self.session.modified = True

    def remove_promo_code(self):
        self.session.pop(self.promo_session_key, None)
        self.session.modified = True

    def promo_code(self):
        return self.session.get(self.promo_session_key, "")
