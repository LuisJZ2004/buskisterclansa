# Django
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist

# My apps
from accounts.models import CustomUser
from genres.models import Genre
from movie_staff.models import MovieStaff
from companies.models import Company

# Movie
class Movie(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, editable=False, blank=False, null=False)
    year = models.DateField(default=timezone.now().date(), blank=False, null=False)
    synopsis = models.TextField(max_length=1000, blank=False, null=False)

    image = models.ImageField(blank=False, default=None)

    genres = models.ManyToManyField(to=Genre)

    created_by = models.ManyToManyField(to=MovieStaff, through="CreatedBy", related_name="movie_created_by")
    directors = models.ManyToManyField(to=MovieStaff, through="Director", related_name="movie_director")
    casts = models.ManyToManyField(to=MovieStaff, through="Cast", related_name="movie_cast")
    producers = models.ManyToManyField(to=MovieStaff, through="Producer", related_name="movie_producer")
    scripts = models.ManyToManyField(to=MovieStaff, through="Script", related_name="movie_script")

    producer_companies = models.ManyToManyField(to=Company, related_name="as_producer")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
    def given_like(self, user_id: int):
        user = CustomUser.objects.get(pk=user_id)

        try:
            user.movielike_set.get(movie__pk=self.pk)
            return True
        except ObjectDoesNotExist:
            return False
        
    def given_dislike(self, user_id: int):
        user = CustomUser.objects.get(pk=user_id)

        try:
            user.moviedislike_set.get(movie__pk=self.pk)
            return True
        except ObjectDoesNotExist:
            return False

class Trailer(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    url = models.URLField(max_length=100, unique=True, blank=False, null=False)


class CreatedBy(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return f"'{self.movie_staff.name}' as creator of '{self.movie.name}'"

class Cast(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return f"'{self.movie_staff.name}' as cast '{self.movie.name}'"
    
class Director(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return f"'{self.movie_staff.name}' as director of '{self.movie.name}'"

class Producer(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return f"'{self.movie_staff.name}' as producer of '{self.movie.name}'"

class Script(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    movie_staff = models.ForeignKey(to=MovieStaff, on_delete=models.CASCADE)

    order = models.IntegerField(default=0, blank=False, null=False)

    def __str__(self) -> str:
        return f"'{self.movie_staff.name}' as script of '{self.movie.name}'"

# Like Dislike
class MovieLike(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} likes '{self.movie.name}'"
    
class MovieDislike(models.Model):
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} dislikes '{self.movie.name}'"