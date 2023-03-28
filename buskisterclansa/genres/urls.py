# Django
from django.urls import path

# This app
from .views import GenreView

app_name="genres"
urlpatterns = [
    path("<slug>/", GenreView.as_view(), name="genre_path"),
]
