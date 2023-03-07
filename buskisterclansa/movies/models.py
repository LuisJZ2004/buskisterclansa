# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Movie(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, editable=False, blank=False, null=False)
    year = models.DateField(default=timezone.now().date(), blank=False, null=False)
    synopsis = models.TextField(max_length=1000, blank=False, null=False)

    image = models.ImageField(blank=False, default=None)

    genres = models.ManyToManyField(to='Genre')

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=False, default=None, editable=False)
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
class MovieStaff(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    bio = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)