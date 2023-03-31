# Django
from django.urls import path

# This app
from .views import SearchView

app_name="search"
urlpatterns = [
    path("", SearchView.as_view(), name="search_path"),
]
