# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView

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