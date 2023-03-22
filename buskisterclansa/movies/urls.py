# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# This app
from .views import MovieView, DragMovieStaffView, LikeDislikeView, MovieReviewsListView, AddReviewView, DeleteReviewView

app_name="movies"
urlpatterns = [
    path("<slug>/<pk>/", MovieView.as_view(), name="movie_path"),
    path("<slug>/<pk>/rate/", login_required(LikeDislikeView.as_view()), name="like_dislike_path"),
    path("<slug>/<pk>/reviews/", MovieReviewsListView.as_view(), name="movie_reviews_path"),
    path("<slug>/<pk>/reviews/add-review/", login_required(AddReviewView.as_view()), name="add_review_path"),
    path("<slug>/<pk>/reviews/delete-review/", login_required(DeleteReviewView.as_view()), name="delete_review_path"),
    path("<slug>/<pk>/drag-staff/<job>/", DragMovieStaffView.as_view(), name="drag_movie_staff_path"),
]
