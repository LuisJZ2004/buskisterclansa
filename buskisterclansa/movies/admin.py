from django.contrib import admin
from .models import Movie, Company
# Register your models here.

admin.site.register(
    (
        Movie, 
        Company
    )
)