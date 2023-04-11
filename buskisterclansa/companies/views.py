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
    
    # The goal of these methods was not to put the direct order name in the enpoints, and instead of that
    # just numbers. Ex: instead of '?order="-year"', this: '?order=0'. So, Users don't put a attribute/query in the
    # endpoint
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
        )[option]
    def __get_orders_by_reviews(self, movies: QuerySet, option: int):
        return (
            sorted(movies, key= lambda t: t.get_reviews_quantity())[::-1],
            sorted(movies, key= lambda t: t.get_reviews_quantity()),
        )[option]

    def get_context_data(self, **kwargs):
        # The filter is just orders
        # if it's by years, they'll be in this var
        movies_with_their_years = None
        # if it's by reviews quantities, they'll be in this var
        movies_with_their_quantities = None

        selected_order = self.request.GET.get("order")

        if selected_order:
            order = int_or_404(selected_order)

            if order == 1 or order == 0:
                # 0 and 1 are years orders
                movies_with_their_years = self.get_object().get_movies_with_their_year(
                    order=self.__get_orders_years_queries(order)
                )
                # 2 and 3 are reviews orders
            elif order == 2 or order == 3:
                movies_with_their_quantities = self.__get_orders_by_reviews(self.get_object().as_producer.all(), order-2)
            else:
                raise Http404
        else:
            # if not selected_order, it is ordered by years, lastest to oldest
            movies_with_their_years = self.get_object().get_movies_with_their_year()

        return {
            self.context_object_name: self.get_object(),
            "years": movies_with_their_years,
            "movies": movies_with_their_quantities,
            "orders": self.__get_orders_dict(),

            "selected_order": selected_order,
        }