# Django
from django.urls import path

# This app
from .views import HomeView

app_name="home"
urlpatterns = [
    path("", HomeView.as_view(), name="home_path"),
]
