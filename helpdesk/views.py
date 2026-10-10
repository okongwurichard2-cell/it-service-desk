from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import PermissionDenied

from .forms import (
    AssetForm,
    LoginForm,
    MaintenanceRecordForm,
    TicketForm,
    TicketUpdateForm,
)

from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import (
    Asset,
    MaintenanceRecord,
    Ticket,
    TicketHistory,
)



User = get_user_model()


class UserLoginView(LoginView):
    template_name = "helpdesk/auth/login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(
            self.request,
            "Welcome back. You have successfully signed in.",
        )
        return super().form_valid(form)

    # def form_invalid(self, form):
    #     messages.error(
    #         self.request,
    #         "Invalid username or password.",
    #     )
    #     return super().form_invalid(form)


class UserLogoutView(LogoutView):

    next_page = "helpdesk:login"

    def dispatch(self, request, *args, **kwargs):
        messages.success(
            request,
            "You have been successfully logged out.",
        )
        return super().dispatch(request, *args, **kwargs)


@login_required
def dashboard(request):

    if request.user.is_superuser:
        role = "Administrator"
    else:
        try:
            role = request.user.staff_profile.get_role_display()
        except AttributeError:
            raise PermissionDenied

    context = {
        "title": "Dashboard",
        "role": role,
        "total_tickets": Ticket.objects.count(),
        "open_tickets": Ticket.objects.filter(
            status="open"
        ).count(),
        "in_progress_tickets": Ticket.objects.filter(
            status="in_progress"
        ).count(),
        "resolved_tickets": Ticket.objects.filter(
            status="resolved"
        ).count(),
        "total_assets": Asset.objects.count(),
        "assigned_assets": Asset.objects.filter(
            status="assigned"
        ).count(),
        "maintenance_assets": Asset.objects.filter(
            status="maintenance"
        ).count(),
        "recent_tickets": Ticket.objects.select_related(
            "requester",
            "assigned_to",
        ).order_by("-created_at")[:5],
    }

    return render(
        request,
        "helpdesk/dashboard.html",
        context,
    )


@login_required
def ticket_list(request):

    if request.user.is_superuser:
        tickets = (
            Ticket.objects
            .select_related(
                "requester",
                "assigned_to",
            )
            .order_by("-created_at")
        )

    else:
        try:
            profile = request.user.staff_profile
        except AttributeError:
            raise PermissionDenied

        if profile.role == "it_staff":
            tickets = (
                Ticket.objects
                .select_related(
                    "requester",
                    "assigned_to",
                )
                .order_by("-created_at")
            )
        else:
            tickets = (
                Ticket.objects
                .filter(requester=request.user)
                .select_related(
                    "requester",
                    "assigned_to",
                )
                .order_by("-created_at")
            )

    status = request.GET.get("status")
    priority = request.GET.get("priority")

    if status:
        tickets = tickets.filter(status=status)

    if priority:
        tickets = tickets.filter(priority=priority)

    context = {
        "title": "Tickets",
        "tickets": tickets,
        "status_choices": Ticket.STATUS_CHOICES,
        "priority_choices": Ticket.PRIORITY_CHOICES,
        "selected_status": status,
        "selected_priority": priority,
    }

    return render(
        request,
        "helpdesk/tickets/list.html",
        context,
    )


@login_required
def ticket_create(request):

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if profile.role != "staff":
        raise PermissionDenied

    if request.method == "POST":
        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.status = "open"
            ticket.save()

            TicketHistory.objects.create(
                ticket=ticket,
                changed_by=request.user,
                old_status="",
                new_status="open",
                note="Ticket created.",
            )

            messages.success(
                request,
                "Support ticket submitted successfully.",
            )

            return redirect(
                "helpdesk:ticket_detail",
                ticket.id,
            )

    else:
        form = TicketForm()

    return render(
        request,
        "helpdesk/tickets/form.html",
        {
            "title": "Create Ticket",
            "heading": "Submit Support Ticket",
            "form": form,
        },
    )


@login_required
def ticket_detail(request, ticket_id):

    ticket = get_object_or_404(
        Ticket.objects.select_related(
            "requester",
            "assigned_to",
        ),
        id=ticket_id,
    )

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    allowed = (
        request.user.is_superuser
        or profile.role == "it_staff"
        or ticket.requester_id == request.user.id
    )

    if not allowed:
        raise PermissionDenied

    can_manage = (
        request.user.is_superuser
        or profile.role == "it_staff"
    )

    update_form = None

    if can_manage:
        update_form = TicketUpdateForm(instance=ticket)

    context = {
        "title": "Ticket Details",
        "ticket": ticket,
        "history": ticket.history.select_related(
            "changed_by"
        ),
        "update_form": update_form,
        "can_manage": can_manage,
    }

    return render(
        request,
        "helpdesk/tickets/detail.html",
        context,
    )


@login_required
@transaction.atomic
def ticket_update(request, ticket_id):

    ticket = get_object_or_404(
        Ticket,
        id=ticket_id,
    )

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if not (
        request.user.is_superuser
        or profile.role == "it_staff"
    ):
        raise PermissionDenied

    if request.method != "POST":
        return redirect(
            "helpdesk:ticket_detail",
            ticket.id,
        )

    old_status = ticket.status

    form = TicketUpdateForm(
        request.POST,
        instance=ticket,
    )

    if form.is_valid():

        updated_ticket = form.save()

        if old_status != updated_ticket.status:

            TicketHistory.objects.create(
                ticket=updated_ticket,
                changed_by=request.user,
                old_status=old_status,
                new_status=updated_ticket.status,
                note="Ticket status updated.",
            )

        messages.success(
            request,
            "Ticket updated successfully.",
        )

    else:

        messages.error(
            request,
            "Ticket could not be updated. Please check the form.",
        )

    return redirect(
        "helpdesk:ticket_detail",
        ticket.id,
    )


@login_required
def asset_list(request):

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if not (
        request.user.is_superuser
        or profile.role == "it_staff"
    ):
        raise PermissionDenied

    assets = (
        Asset.objects
        .select_related("assigned_to")
        .order_by("asset_tag")
    )

    status = request.GET.get("status")
    category = request.GET.get("category")

    if status:
        assets = assets.filter(status=status)

    if category:
        assets = assets.filter(category=category)

    context = {
        "title": "Assets",
        "assets": assets,
        "status_choices": Asset.STATUS_CHOICES,
        "category_choices": Asset.CATEGORY_CHOICES,
        "selected_status": status,
        "selected_category": category,
    }

    return render(
        request,
        "helpdesk/assets/list.html",
        context,
    )


@login_required
def asset_create(request):

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if not (
        request.user.is_superuser
        or profile.role == "it_staff"
    ):
        raise PermissionDenied

    if request.method == "POST":
        form = AssetForm(request.POST)

        if form.is_valid():
            asset = form.save()

            if asset.assigned_to:
                asset.status = "assigned"
                asset.save(update_fields=["status"])

            messages.success(
                request,
                "Asset added successfully.",
            )

            return redirect(
                "helpdesk:asset_detail",
                asset.id,
            )

    else:
        form = AssetForm()

    return render(
        request,
        "helpdesk/assets/form.html",
        {
            "title": "Add Asset",
            "form": form,
        },
    )


@login_required
def asset_detail(request, asset_id):

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if not (
        request.user.is_superuser
        or profile.role == "it_staff"
    ):
        raise PermissionDenied

    asset = get_object_or_404(
        Asset.objects.select_related("assigned_to"),
        id=asset_id,
    )

    maintenance_records = (
        asset.maintenance_records
        .select_related("performed_by")
        .all()
    )

    return render(
        request,
        "helpdesk/assets/detail.html",
        {
            "title": "Asset Details",
            "asset": asset,
            "maintenance_records": maintenance_records,
        },
    )


@login_required
def asset_maintenance(request, asset_id):

    try:
        profile = request.user.staff_profile
    except AttributeError:
        raise PermissionDenied

    if not (
        request.user.is_superuser
        or profile.role == "it_staff"
    ):
        raise PermissionDenied

    asset = get_object_or_404(
        Asset,
        id=asset_id,
    )

    if request.method == "POST":
        form = MaintenanceRecordForm(request.POST)

        if form.is_valid():
            record = form.save(commit=False)
            record.asset = asset
            record.performed_by = request.user
            record.save()

            asset.status = "maintenance"
            asset.save(update_fields=["status"])

            messages.success(
                request,
                "Maintenance record added successfully.",
            )

            return redirect(
                "helpdesk:asset_detail",
                asset.id,
            )

    else:
        form = MaintenanceRecordForm()

    return render(
        request,
        "helpdesk/assets/form.html",
        {
            "title": "Add Maintenance Record",
            "form": form,
            "asset": asset,
            "maintenance_form": True,
        },
    )