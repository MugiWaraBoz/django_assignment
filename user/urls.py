from django.urls import path, include
from user.views import sign_in, sign_out, sign_up, activate_account, user_dashboard, admin_dashboard, organizer_dashboard

urlpatterns = [
    path("sign-up/", sign_up, name = "sign-up"), 
    path("sign-in/", sign_in, name = "sign-in"),
    path("sign-out/", sign_out, name = "sign-out"),
    path("admin-dashboard/<int:id>", admin_dashboard, name = "admin-dashboard"), 
    path("organizer-dashboard/<int:id>", organizer_dashboard, name = "organizer-dashboard"),
    path("user-dashboard/<int:id>", user_dashboard, name = "user-dashboard"),
    path("activate/<int:uid>/<str:token>/", activate_account, name="activate_account")
    
]

