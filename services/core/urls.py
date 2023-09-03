from django.urls import re_path

from services.core.views.user import RegisterUserView, LoginUserView, LogoutUserView
from services.core.views.file import ListFileView, FileView
from services.core.views.directory import DirectoryView

app_name = "core"

urlpatterns = [
    re_path(r"^user/register/?$", RegisterUserView.as_view(), name="register-user"),
    re_path(r"^user/login/?$", LoginUserView.as_view(), name="login-user"),
    re_path(r"^user/logout/?$", LogoutUserView.as_view(), name="logout-user"),
    re_path(r"^list-files/?$", ListFileView.as_view(), name="list-files"),
    re_path(r"^file/?$", FileView.as_view(), name="file"),
    re_path(r"^directory/(?P<id>\d+)?$", DirectoryView.as_view(), name="directory")
]
