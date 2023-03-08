# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Movie
class Movie(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, editable=False, blank=False, null=False)
    year = models.DateField(default=timezone.now().date(), blank=False, null=False)
    synopsis = models.TextField(max_length=1000, blank=False, null=False)

    image = models.ImageField(blank=False, default=None)

    genres = models.ManyToManyField(to='Genre')

    created_by = models.ManyToManyField(to="MovieStaff", through="CreatedBy", related_name="movie_created_by")
    directors = models.ManyToManyField(to="MovieStaff", through="Director", related_name="movie_director")
    casts = models.ManyToManyField(to="MovieStaff", through="Cast", related_name="movie_cast")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

# Genre  
class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=False, default=None, editable=False)
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

# MovieStaff
class MovieStaff(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    bio = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)

class CreatedBy(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(unique=True, default=0, blank=False, null=False)

class Cast(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(unique=True, default=0, blank=False, null=False)

class Director(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(unique=True, default=0, blank=False, null=False)

# Company