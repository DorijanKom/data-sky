from django.urls import re_path
from services.core.views.ok import OkView

from services.core.views.user_authentication import RegisterUserView, LoginUserView

app_name = "core"

urlpatterns = [
    re_path(r"^ok/?$", OkView.as_view(), name="ok"),
    re_path(r"^user/register/?$", RegisterUserView.as_view(), name="register-user"),
    re_path(r"^user/login/?$", LoginUserView.as_view(), name="login-user"),

]
