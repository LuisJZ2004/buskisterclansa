from django.contrib import admin
from .models import Movie, Genre, MovieStaff
# Register your models here.

admin.site.register(
    (
        Movie, 
        Genre, 
        MovieStaff
    )
)