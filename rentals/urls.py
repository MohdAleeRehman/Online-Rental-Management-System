from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("item/<int:pk>/", views.item_detail, name="item_detail"),
    path("item/<int:pk>/request/", views.request_rental, name="request_rental"),
    path("add_item/", views.add_item, name="add_item"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("search/", views.search_items, name="search_items"),
    path("cancel_request/<int:pk>/", views.cancel_request, name="cancel_request"),
    path("manage_items/", views.manage_items, name="manage_items"),
    path("update_item_status/<int:pk>/<str:status>/", views.update_item_status, name="update_item_status"),
    path("user/<int:user_id>/", views.user_profile, name="user_profile"),
    path("rental_request/<int:rental_request_id>/confirm_return/", views.confirm_return, name="confirm_return",),
    path("edit-item/<int:pk>/", views.edit_item, name="edit_item"),
    path("delete-item/<int:pk>/", views.delete_item, name="delete_item"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
]
