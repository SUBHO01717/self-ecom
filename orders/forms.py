from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "email", "shipping_address", "payment_method", "transaction_id"]
        widgets = {"shipping_address": forms.Textarea(attrs={"rows": 4})}

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get("payment_method")
        transaction_id = cleaned.get("transaction_id")
        if method in {Order.PaymentMethod.BKASH, Order.PaymentMethod.NAGAD} and not transaction_id:
            raise forms.ValidationError("Transaction ID is required for manual mobile payments.")
        return cleaned
