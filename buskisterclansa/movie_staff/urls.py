# Django
from django.urls import path

# This app
from .views import MovieStaffView

app_name="movie_staff"
urlpatterns = [
    path("<slug>/<pk>/", MovieStaffView.as_view(), name="movie_staff_path"),
]
