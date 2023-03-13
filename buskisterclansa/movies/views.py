# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.http import Http404

# This app
from .models import Movie

class MovieView(DetailView):
    model=Movie
    template_name="movies/movie.html"
    context_object_name = "movie"

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get("part"):
            return super().dispatch(request, *args, **kwargs)
        
        raise Http404

    def get_queryset(self):
        return self.model.objects.all()

    def get_object(self, *args, **kwargs):
        return get_object_or_404(self.get_queryset(), pk=self.kwargs.get("pk"), slug=self.kwargs.get("slug"))