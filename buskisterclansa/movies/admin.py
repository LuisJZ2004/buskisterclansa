from django.contrib import admin
from .models import Movie, Cast, CreatedBy, Director, Script, Producer, Trailer, Review
# Register your models here.

admin.site.register(
    (
        Movie,
        Cast, 
        CreatedBy, 
        Director, 
        Script, 
        Producer,
        Trailer,
        Review,
    )
)