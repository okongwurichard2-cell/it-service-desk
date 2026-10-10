from django.contrib.auth.models import User
from django.db import models


class StaffProfile(models.Model):

    ROLE_CHOICES = [
        ("staff", "Staff"),
        ("it_staff", "IT Staff"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="staff",
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    def __str__(self):
        return (
            f"{self.user.get_full_name()} "
            f"- {self.get_role_display()}"
        )


class Ticket(models.Model):

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("assigned", "Assigned"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    requester = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="submitted_tickets",
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.title


class TicketHistory(models.Model):

    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="history",
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    old_status = models.CharField(
        max_length=20,
        blank=True,
    )

    new_status = models.CharField(
        max_length=20,
    )

    note = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.ticket} - {self.new_status}"


class Asset(models.Model):

    CATEGORY_CHOICES = [
        ("computer", "Computer"),
        ("printer", "Printer"),
        ("network", "Network Device"),
        ("accessory", "Accessory"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("assigned", "Assigned"),
        ("maintenance", "Under Maintenance"),
        ("retired", "Retired"),
    ]

    asset_tag = models.CharField(
        max_length=50,
        unique=True,
    )

    name = models.CharField(
        max_length=150,
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    serial_number = models.CharField(
        max_length=100,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_assets",
    )

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"{self.asset_tag} - {self.name}"


class MaintenanceRecord(models.Model):

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="maintenance_records",
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )

    description = models.TextField()

    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    maintenance_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-maintenance_date"]

    def __str__(self):
        return (
            f"{self.asset.asset_tag} "
            f"- {self.maintenance_date}"
        )