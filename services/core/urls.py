from django.urls import re_path

from services.core.views.user import RegisterUserView, LoginUserView, LogoutUserView
from services.core.views.file import ListFileView

app_name = "core"

urlpatterns = [
    re_path(r"^user/register/?$", RegisterUserView.as_view(), name="register-user"),
    re_path(r"^user/login/?$", LoginUserView.as_view(), name="login-user"),
    re_path(r"^user/logout/?$", LogoutUserView.as_view(), name="logout-user"),
    re_path(r"^list-files/?$", ListFileView.as_view(), name="list-files")
]
