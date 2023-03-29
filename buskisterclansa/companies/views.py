# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView

# This app
from .models import Company

class CompanyView(DetailView):
    model=Company
    template_name="companies/company.html"
    context_object_name="company"

    def get_queryset(self):
        return self.model.objects.all()
    def get_object(self, *args, **kwargs):
        return get_object_or_404(klass=self.get_queryset(), slug=self.kwargs.get("slug"))
    def get_context_data(self, **kwargs):
        print(self.get_object().get_movies_sorted_by_year())
        return {
            self.context_object_name: self.get_object(),
            "movies": self.get_object().as_producer.all().order_by("year"),
            "years": self.get_object().get_movies_sorted_by_year(),
        }