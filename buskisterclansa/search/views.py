# Django
from django.shortcuts import render, redirect
from django.views.generic import View

# My apps
from movies.models import Movie
from movie_staff.models import MovieStaff

class SearchView(View):
    template_name="search/search.html"
    
    def get(self, request, *args, **kwargs):

        if not request.GET.get("search-bar"):
            return redirect(to="home:home_path")

        search = request.GET.get("search-bar")

        movies = Movie.objects.filter(name__icontains=search)
        staff = MovieStaff.objects.filter(name__icontains=search)

        return render(
            request=request,
            template_name=self.template_name,
            context={
                "search": request.GET.get("search-bar"),
                "movies": movies,
                "staff": staff,
            }
        )