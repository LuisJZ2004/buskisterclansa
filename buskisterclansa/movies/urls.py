# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# This app
from .views import MovieView, DragMovieStaffView

app_name="movies"
urlpatterns = [
    path("<slug>/<pk>/", MovieView.as_view(), name="movie_path"),
    path("<slug>/<pk>/drag-staff", login_required(DragMovieStaffView.as_view()), name="drag_movie_staff_path"),
]
