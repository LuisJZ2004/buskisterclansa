# Django
from django.shortcuts import render
from django.views.generic import View

# My apps
from movies.models import Movie
from movie_staff.models import MovieStaff

class SearchView(View):
    template_name="search/search.html"
    
    def get(self, request, *args, **kwargs):
        return render(
            request=request,
            template_name=self.template_name,
            context={
                
            }
        )