from django import forms
from django.contrib.auth import authenticate


class CustomerLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or phone")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        identifier = cleaned.get("identifier")
        password = cleaned.get("password")
        if identifier and password:
            user = authenticate(username=identifier, password=password)
            if user is None:
                from django.contrib.auth.models import User

                match = User.objects.filter(customer_profile__phone=identifier).first() or User.objects.filter(email__iexact=identifier).first()
                if match:
                    user = authenticate(username=match.username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid login details.")
            cleaned["user"] = user
        return cleaned
