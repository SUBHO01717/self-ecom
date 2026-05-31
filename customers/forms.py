from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class CustomerLoginForm(forms.Form):
    identifier = forms.CharField(label="Email or phone")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()

        identifier = cleaned.get("identifier")
        password = cleaned.get("password")

        if not identifier or not password:
            return cleaned

        # Try direct login first
        user = authenticate(
            username=identifier,
            password=password
        )

        match = None

        # Lookup by phone or email
        if user is None:
            match = (
                User.objects.filter(
                    customer_profile__phone=identifier
                ).first()
                or
                User.objects.filter(
                    email__iexact=identifier
                ).first()
            )

            if match:

                # Account exists but password not yet created
                if not match.has_usable_password():
                    raise forms.ValidationError(
                        "Your account was created during checkout. Please set your password first."
                    )

                user = authenticate(
                    username=match.username,
                    password=password
                )

        if user is None:
            raise forms.ValidationError(
                "Invalid login details."
            )

        cleaned["user"] = user
        return cleaned


class ActivateAccountForm(forms.Form):
    identifier = forms.CharField(
        label="Email or Phone"
    )

    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned = super().clean()

        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Passwords do not match."
            )

        identifier = cleaned.get("identifier")

        if identifier:
            user = (
                User.objects.filter(
                    customer_profile__phone=identifier
                ).first()
                or
                User.objects.filter(
                    email__iexact=identifier
                ).first()
            )

            if not user:
                raise forms.ValidationError(
                    "No account found with this email or phone number."
                )

            cleaned["user"] = user

        return cleaned