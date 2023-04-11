from django.contrib import admin
from .models import Movie, Cast, Director, Script, Producer, Review, ReviewComment
# Register your models here.

admin.site.register(
    (
        Movie,
        Cast, 
        Director, 
        Script, 
        Producer,
        Review,
        ReviewComment,
    )
)