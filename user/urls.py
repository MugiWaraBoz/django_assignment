from django.urls import path, include
from user.views import change_user_group, manage_roles, organizers, role_details, role_details, participants, sign_in, sign_out, sign_up, activate_account, user_dashboard, admin_dashboard, organizer_dashboard

urlpatterns = [
    path("sign-up/", sign_up, name = "sign-up"), 
    path("sign-in/", sign_in, name = "sign-in"),
    path("sign-out/", sign_out, name = "sign-out"),
    
    path("admin-dashboard/", admin_dashboard, name = "admin-dashboard"), 
    path("admin-dashboard/manage-roles/", manage_roles, name = "manage-roles"),
    path("admin-dashboard/organizers/", organizers, name = "organizers"),
    path("admin-dashboard/participants/", participants, name = "participants"),
    path("admin-dashboard/role-details/", role_details, name = "role-details"),
    path("admin-dashboard/change-user-group/<int:user_id>/", change_user_group, name="change-user-group"),

    path("organizer-dashboard/<int:id>/", organizer_dashboard, name = "organizer-dashboard"),
    path("user-dashboard/<int:id>/", user_dashboard, name = "user-dashboard"),
    path("activate/<int:uid>/<str:token>/", activate_account, name="activate_account")
    
]

