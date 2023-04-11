# Django
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# My apps
from movies import models as MovieModels

class MovieStaff(models.Model):
    name = models.CharField(max_length=70, blank=False, null=False)
    slug = models.SlugField(max_length=70, blank=False, null=False, editable=False)
    bio = models.TextField(max_length=1000, blank=False, null=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)
    
    def get_total_review_of_this_staff_movie(self):
        """
        returns the total reviews of all the movies in which this staff is
        """
        movies = MovieModels.Movie.objects.filter(
            models.Q(directors__name = self.name) |
            models.Q(casts__name = self.name) |
            models.Q(producers__name = self.name) |
            models.Q(scripts__name = self.name)
        )
        total = 0

        for movie in movies:
            total += movie.get_reviews_quantity()

        return total