from django.contrib import admin
from .models import Movie, Genre, MovieStaff, Company
# Register your models here.

admin.site.register(
    (
        Movie, 
        Genre, 
        MovieStaff,
        Company
    )
)