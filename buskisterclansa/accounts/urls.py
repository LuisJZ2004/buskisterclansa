# Django
from django.urls import path
from django.contrib.auth.views import LogoutView

# This app
from .views import SingInView, CustomLoginView

app_name="accounts"
urlpatterns = [
    path("login/", CustomLoginView.as_view(template_name="accounts/register.html"), name="login_path"),
    path("sign-in/", SingInView.as_view(), name="sign_in_path"),
]
