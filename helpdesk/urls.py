from django.urls import path

from .views import (
    UserLoginView,
    UserLogoutView,
    dashboard,
    ticket_list,
    ticket_create,
    ticket_detail,
    ticket_update,

    asset_list,
    asset_create,
    asset_detail,
    asset_maintenance,
)


app_name = "helpdesk"


urlpatterns = [
    path(
        "login/",
        UserLoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        UserLogoutView.as_view(),
        name="logout",
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),

    path(
        "tickets/",
        ticket_list,
        name="ticket_list",
    ),

    path(
        "tickets/create/",
        ticket_create,
        name="ticket_create",
    ),

    path(
        "tickets/<int:ticket_id>/",
        ticket_detail,
        name="ticket_detail",
    ),

    path(
        "tickets/<int:ticket_id>/update/",
        ticket_update,
        name="ticket_update",
    ),

    path(
        "assets/",
        asset_list,
        name="asset_list",
    ),

    path(
        "assets/create/",
        asset_create,
        name="asset_create",
    ),

    path(
        "assets/<int:asset_id>/",
        asset_detail,
        name="asset_detail",
    ),

    path(
        "assets/<int:asset_id>/maintenance/",
        asset_maintenance,
        name="asset_maintenance",
    ),
]