# Django
from django.urls import path
from django.contrib.auth.decorators import login_required

# This app
from .views import (
    MovieView, 
    DragMovieStaffView, 
    MovieReviewsListView, 
    AddReviewView, 
    DeleteReviewView, 
    ReviewDetailView,
    LikeDislikeReviewView,
    AddCommentReviewView,
    StaffOfAMovieView,
)
app_name="movies"
urlpatterns = [
    path("<slug>/<pk>/", MovieView.as_view(), name="movie_path"),
    path("<slug>/<pk>/staff/<job>/", StaffOfAMovieView.as_view(), name="staff_of_a_movie_path"),
    path("<slug>/<pk>/reviews/", MovieReviewsListView.as_view(), name="movie_reviews_path"),
    path("<slug>/<pk>/reviews/add-review/", login_required(AddReviewView.as_view()), name="add_review_path"),
    path("<slug>/<pk>/reviews/delete-review/", login_required(DeleteReviewView.as_view()), name="delete_review_path"),
    path("<slug>/<pk>/reviews/<review_pk>/", ReviewDetailView.as_view(), name="review_path"),
    path("<slug>/<pk>/reviews/<review_pk>/rate/", login_required(LikeDislikeReviewView.as_view()), name="rate_review_path"),
    path("<slug>/<pk>/reviews/<review_pk>/add-comment/", login_required(AddCommentReviewView.as_view()), name="add_comment_review_path"),
    path("<slug>/<pk>/drag-staff/<job>/", DragMovieStaffView.as_view(), name="drag_movie_staff_path"),
]
