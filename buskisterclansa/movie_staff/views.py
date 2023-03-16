# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

# This app
from .models import MovieStaff

class MovieStaffView(DetailView):
    model = MovieStaff
    context_object_name = "staff"

    def get_queryset(self):
        return self.model.objects.all()
    
    def get_object(self, *args, **kwargs):
        return get_object_or_404(klass=self.get_queryset(), slug=self.kwargs.get("slug"), pk=self.kwargs.get("pk"))