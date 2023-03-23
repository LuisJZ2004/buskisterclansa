# Django
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, View
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

# My apps
from extra_logic.movies.functions import get_dependant_object_if_it_exist

# This app
from .models import Movie, MovieLike, MovieDislike, Review
from .forms import ReviewForm

class MovieView(DetailView):
    model=Movie
    template_name="movies/movie.html"
    context_object_name = "movie"

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"), slug=self.kwargs.get("slug"))
    
    def get_context_data(self, **kwargs):

        context = {
            self.context_object_name: self.get_object(),
            "directors": self.get_object().directors.all().order_by("director__order"),
            "created_by": self.get_object().created_by.all().order_by("createdby__order"),
            "script": self.get_object().scripts.all().order_by("script__order"),
            "producers": self.get_object().producers.all().order_by("producer__order"),
            "cast": self.get_object().casts.all().order_by("cast__order")[:3],
            "companies": self.get_object().producer_companies.all(),
            "cast_len": len(self.get_object().casts.all().order_by("cast__order")),
            "movie_pk": self.kwargs.get("pk"),
            "movie_slug": self.kwargs.get("slug"),

            "reviews": self.get_object().review_set.all().order_by("-pub_date")[:5],
            "stars_rating": (
                "",
                len(self.get_object().review_set.filter(rate_by_stars=1)),
                len(self.get_object().review_set.filter(rate_by_stars=2)),
                len(self.get_object().review_set.filter(rate_by_stars=3)),
                len(self.get_object().review_set.filter(rate_by_stars=4)),
                len(self.get_object().review_set.filter(rate_by_stars=5)),
            )
        }
        
        return context
    
class DragMovieStaffView(View):

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(klass=Movie, pk=kwargs.get("pk"), slug=kwargs.get("slug"))
        if request.user.is_authenticated:
            if request.user.is_admin:
                return super().dispatch(request, *args, **kwargs)

        raise Http404

    def __get_relation_staff(self):
        return {
                "created_by": self.movie.createdby_set.all().order_by("order"),
                "cast": self.movie.cast_set.all().order_by("order"),
                "director": self.movie.director_set.all().order_by("order"),
                "producer": self.movie.producer_set.all().order_by("order"),
                "script": self.movie.script_set.all().order_by("order"),
            }

    def get(self, request, *args, **kwargs):
        
        if not self.__get_relation_staff().get(self.kwargs.get("job")):
            raise Http404

        return render(
            request=request,
            template_name="movies/drag_movie_staff.html",
            context={
                "objects": self.__get_relation_staff()[self.kwargs.get("job")], 
                "job": self.kwargs.get("job"),
                "pk": self.kwargs.get("pk"),
                "slug": self.kwargs.get("slug"),
            }
        )
    
    def post(self, request, *args, **kwargs):
        staff = self.__get_relation_staff().get(self.kwargs.get("job"))
        if not staff:
            raise Http404
        request_post = dict(request.POST)
        request_post.pop("csrfmiddlewaretoken")

        iterator = 0
        for person_id in request_post.values():
            person = staff.get(id=person_id[0])
            person.order = iterator
            person.save()
            iterator += 1

        return redirect(to="movies:drag_movie_staff_path", slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"), job=self.kwargs.get("job") )

class LikeDislikeView(View):
    def post(self, request, *args, **kwargs):
        movie = get_object_or_404(klass=Movie, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        
        
        if request.POST.get("rate") == "like":
            try:
                like = movie.movielike_set.get(user__pk=request.user.pk)
                like.delete()
            except ObjectDoesNotExist:
                try:
                    dislike = movie.moviedislike_set.get(user__pk=request.user.pk)
                    dislike.delete()
                except ObjectDoesNotExist:
                    pass
                movie.movielike_set.create(user=request.user)
        elif request.POST.get("rate") == "dislike":
            try:
                dislike = movie.moviedislike_set.get(user__pk=request.user.pk)
                dislike.delete()
            except ObjectDoesNotExist:
                try:
                    like = movie.movielike_set.get(user__pk=request.user.pk)
                    like.delete()
                except ObjectDoesNotExist:
                    pass
                movie.moviedislike_set.create(user=request.user)

        return redirect(to="movies:movie_path", slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
    
class MovieReviewsListView(ListView):
    template_name = "movies/reviews.html"
    context_object_name = "reviews"

    def __get_orders_indexes(self):
        return {
            "stars (higher to lower)": "0",
            "stars (lower to higher)": "1",
        }
    def __get_orders_queries(self, ):
        return (
            "-rate_by_stars",
            "rate_by_stars",
        )
    def __get_index_order_or_404(self):
        try:
            return self.__get_orders_queries()[int(self.request.GET.get("order"))]
        except ValueError:
            raise Http404
        
    def __get_filters(self):
        return {
            "5 stars": "5",
            "4 stars": "4",
            "3 stars": "3",
            "2 stars": "2",
            "1 stars": "1",
        }

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(klass=Movie, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.movie.review_set.all()

    def get_context_data(self, **kwargs):

        reviews = self.get_queryset()

        if not self.request.GET.get("filter") and not self.request.GET.get("order"):
            reviews = reviews.order_by("-pub_date")

        if self.request.GET.get("filter"):
            try:
                reviews = reviews.filter(rate_by_stars=int(self.request.GET.get("filter")))
            except ValueError:
                raise Http404
        if self.request.GET.get("order"):
            reviews = reviews.order_by(self.__get_index_order_or_404())

        print(type(self.request.GET.get("order")))
        print(self.request.GET.get("order") == str(self.__get_orders_indexes()["stars (higher to lower)"]))
        return {
            self.context_object_name: reviews,
            "movie": self.movie,
            "stars_rating": (
                "",
                len(self.movie.review_set.filter(rate_by_stars=1)),
                len(self.movie.review_set.filter(rate_by_stars=2)),
                len(self.movie.review_set.filter(rate_by_stars=3)),
                len(self.movie.review_set.filter(rate_by_stars=4)),
                len(self.movie.review_set.filter(rate_by_stars=5)),
            ),
            "orders": self.__get_orders_indexes(),
            "filters": self.__get_filters(),

            "selected_order": str(self.request.GET.get("order")),
            "selected_filter": self.request.GET.get("filter"),
        }
    
class AddReviewView(View):

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(klass=Movie, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        self.comment = get_dependant_object_if_it_exist(self.movie.review_set, request.user.pk, "user__pk")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name="movies/add_review.html",
            context= {
                "movie_name": self.movie.name,
                "movie_slug": self.kwargs.get("slug"),
                "movie_pk": self.kwargs.get("pk"),
                "comment": self.comment,
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)

        if form.is_valid():
            if self.comment:
                self.comment.name=request.POST["name"]
                self.comment.content=request.POST["content"]
                self.comment.rate_by_stars=request.POST["rate_by_stars"]
                self.comment.save()
            else:
                self.movie.review_set.create(
                    user=request.user,
                    name=request.POST["name"],
                    content=request.POST["content"],
                    rate_by_stars=request.POST["rate_by_stars"],
                )
            return redirect(to="movies:movie_path", slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        else:
            return render(
                request=request,
                template_name="movies/add_review.html",
                context= {
                    "movie_name": self.movie.name,
                    "movie_slug": self.kwargs.get("slug"),
                    "movie_pk": self.kwargs.get("pk"),
                    "comment": self.comment,
                    "errors": dict(form.errors),
                }
            )
        
class DeleteReviewView(View):
    def post(self, request, *args, **kwargs):
        self.movie = get_object_or_404(klass=Movie, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        self.comment = get_dependant_object_if_it_exist(self.movie.review_set, request.user.pk, "user__pk")

        if self.comment: 
            self.comment.delete()
        
        return redirect(to="movies:movie_path", slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))

class ReviewDetailView(DetailView):
    template_name="movies/show_review.html"
    context_object_name="review"

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(klass=Movie, slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.movie.review_set.all()
    
    def get_object(self, *args, **kwargs):
        return get_object_or_404(klass=self.get_queryset(), pk=self.kwargs.get("review_pk"))
    
    def get_context_data(self, **kwargs):
        return {
            self.context_object_name: self.get_object(),
            "movie": self.movie,
        }