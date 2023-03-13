# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# This app
from .models import Movie

class MovieView(DetailView):
    model=Movie
    template_name="movies/movie.html"
    context_object_name = "movie"

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"), slug=self.kwargs.get("slug"))