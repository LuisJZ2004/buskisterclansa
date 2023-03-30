# Django
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, DetailView
from django.db.models import QuerySet
from django.http import Http404

# My apps
from extra_logic.functions import int_or_404

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
    
    def __get_orders_dict(self):
        return {
            "years (recent to old)": "0",
            "years (old to recent)": "1",
            "reviews (most rated)": "2",
            "reviews (less rated)": "3",
        }
    def __get_orders_years_queries(self, option: int):
        return (
            "-year",
            "year",
            # movies.objects.all().order_by("-years"),
            # movies.objects.all().order_by("years"),
            # sorted(movies.objects.all(), key= lambda t: t.get_reviews_quantity())[::-1],
            # sorted(movies.objects.all(), key= lambda t: t.get_reviews_quantity()),
        )[option]
    def __get_orders_by_reviews(self, movies: QuerySet, option: int):
        return (
            sorted(movies, key= lambda t: t.get_reviews_quantity())[::-1],
            sorted(movies, key= lambda t: t.get_reviews_quantity()),
        )[option]

    def get_context_data(self, **kwargs):
        
        movies_with_their_years = None
        movies_with_their_quantities = None

        if self.request.GET.get("order"):
            order = int_or_404(self.request.GET.get("order"))

            if order == 1 or order == 0:
                movies_with_their_years = self.get_object().get_movies_with_their_year(
                    order=self.__get_orders_years_queries(order)
                )
            elif order == 2 or order == 3:
                movies_with_their_quantities = self.__get_orders_by_reviews(self.get_object().as_producer.all(), order-2)
            else:
                raise Http404
        else:
            movies_with_their_years = self.get_object().get_movies_with_their_year()

        return {
            self.context_object_name: self.get_object(),
            "years": movies_with_their_years,
            "movies": movies_with_their_quantities,
            "orders": self.__get_orders_dict()
        }