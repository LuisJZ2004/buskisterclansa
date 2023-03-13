# Django
from django.urls import path

# This app
from .views import MovieView

app_name="movies"
urlpatterns = [
    path("<slug>/<pk>/", MovieView.as_view(), name="movie_path"),
]
