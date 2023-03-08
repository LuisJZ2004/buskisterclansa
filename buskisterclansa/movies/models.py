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
    producers = models.ManyToManyField(to="MovieStaff", through="Producer", related_name="movie_producer")
    scripts = models.ManyToManyField(to="MovieStaff", through="Script", related_name="movie_script")

    producer_companies = models.ManyToManyField(to="Company", related_name="as_producer")
    distributor_companies = models.ManyToManyField(to="Company", related_name="as_distributor")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

class Trailer(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    url = models.URLField(max_length=100, unique=True, blank=False, null=False)

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

class Producer(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(unique=True, default=0, blank=False, null=False)

class Script(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(unique=True, default=0, blank=False, null=False)

# Company
class Company(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=False, null=False, editable=False)
    description = models.TextField(max_length=200, blank=False, null=False)

    image = models.ImageField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    