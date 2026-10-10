from django.contrib import admin

from .models import (
    StaffProfile,
    Ticket,
    TicketHistory,
    Asset,
    MaintenanceRecord,
)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "department",
        "phone",
    )
    list_filter = ("role", "department")
    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "requester",
        "assigned_to",
        "priority",
        "status",
        "created_at",
    )
    list_filter = (
        "priority",
        "status",
    )
    search_fields = (
        "title",
        "description",
        "requester__username",
        "assigned_to__username",
    )
    list_select_related = (
        "requester",
        "assigned_to",
    )


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "changed_by",
        "old_status",
        "new_status",
        "created_at",
    )
    list_filter = (
        "new_status",
    )
    search_fields = (
        "ticket__title",
        "changed_by__username",
        "note",
    )
    list_select_related = (
        "ticket",
        "changed_by",
    )


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "asset_tag",
        "name",
        "category",
        "status",
        "assigned_to",
        "purchase_date",
    )
    list_filter = (
        "category",
        "status",
    )
    search_fields = (
        "asset_tag",
        "name",
        "serial_number",
        "assigned_to__username",
    )
    list_select_related = (
        "assigned_to",
    )


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = (
        "asset",
        "performed_by",
        "maintenance_date",
        "cost",
    )
    list_filter = (
        "maintenance_date",
    )
    search_fields = (
        "asset__asset_tag",
        "asset__name",
        "performed_by__username",
        "description",
    )
    list_select_related = (
        "asset",
        "performed_by",
    )