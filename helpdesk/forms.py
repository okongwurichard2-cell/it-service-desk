from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import (
    Asset,
    MaintenanceRecord,
    Ticket,
)


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your username",
                "autocomplete": "username",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
                "autocomplete": "current-password",
            }
        )
    )

class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "priority",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Describe the issue briefly",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 6,
                    "placeholder": "Explain the issue in detail",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }


class TicketUpdateForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = [
            "assigned_to",
            "status",
            "priority",
        ]

        widgets = {
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "priority": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].queryset = (
            self.fields["assigned_to"]
            .queryset
            .filter(
                staff_profile__role="it_staff"
            )
            .select_related("staff_profile")
            .order_by(
                "last_name",
                "first_name",
                "username",
            )
        )

        self.fields["assigned_to"].empty_label = "Unassigned"


class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = [
            "asset_tag",
            "name",
            "category",
            "serial_number",
            "status",
            "assigned_to",
            "purchase_date",
            "notes",
        ]

        widgets = {
            "asset_tag": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. AST-0026",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Dell Latitude 5420",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "serial_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Serial number",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "assigned_to": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "purchase_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Additional notes",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_to"].queryset = (
            User.objects
            .filter(
                staff_profile__role__in=[
                    "staff",
                    "it_staff",
                ]
            )
            .select_related("staff_profile")
            .order_by(
                "last_name",
                "first_name",
                "username",
            )
        )

        self.fields["assigned_to"].empty_label = "Unassigned"


class MaintenanceRecordForm(forms.ModelForm):

    class Meta:
        model = MaintenanceRecord
        fields = [
            "description",
            "cost",
            "maintenance_date",
        ]

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Describe the maintenance performed",
                }
            ),
            "cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "min": "0",
                    "placeholder": "0.00",
                }
            ),
            "maintenance_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                }
            ),
        }