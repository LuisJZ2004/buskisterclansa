# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from django.http import Http404

# This app
from .models import Genre

class GenreView(DetailView):
    model=Genre
    template_name="genres/genre.html"
    context_object_name="genre"

    def get_queryset(self):
        return self.model.objects.all()
    def get_object(self):
        return get_object_or_404(klass=self.get_queryset(), slug=self.kwargs.get("slug"))
    def get(self, request, *args, **kwargs):
        if not request.GET.get("rate"):
            raise Http404
        return super().get(request, *args, **kwargs)
    
    def __get_movies(self, option: str):
        """
        get movies sorted by the sent option
        """
        if option == "best-rated":
            return sorted(
                self.get_object().movie_set.all(),
                key=lambda q: q.get_stars_quantity(star=5)
            )[::-1][:50]
        elif option == "worst-rated":
            return sorted(
                self.get_object().movie_set.all(),
                key=lambda q: q.get_stars_quantity(star=1)
            )[::-1][:50]
        elif option == "most-rated":
            return sorted(
                self.get_object().movie_set.all(),
                key=lambda q: q.get_reviews_quantity()
            )[::-1][:50]
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        return {
            self.context_object_name: self.get_object(),
            "movies": self.__get_movies(self.request.GET.get("rate"))
        }