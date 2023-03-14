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
    
    def get_context_data(self, **kwargs):

        context = {
            self.context_object_name: self.get_object(),
            "directors": self.get_object().directors.all().order_by("director__order"),
            "created_by": self.get_object().created_by.all().order_by("createdby__order"),
            "script": self.get_object().scripts.all().order_by("script__order"),
            "producers": self.get_object().producers.all().order_by("producer__order"),
            "cast": self.get_object().casts.all().order_by("cast__order")[:5],
            "companies": self.get_object().producer_companies.all(),
            "cast_len": len(self.get_object().casts.all().order_by("cast__order")),
        }

        return context