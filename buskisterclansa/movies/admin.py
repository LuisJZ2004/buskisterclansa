from django.contrib import admin
from .models import Movie, Cast, CreatedBy, Director, Script, Producer, Trailer, Review, ReviewComment
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
        ReviewComment,
    )
)