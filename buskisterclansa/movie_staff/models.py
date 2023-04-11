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
    
    def get_all_movies(self):

        movies = [
            self.movie_director.all().order_by("year"),
            self.movie_script.all().order_by("year"),
            self.movie_producer.all().order_by("year"),
            self.movie_cast.all().order_by("year"),
        ]

        final_movies = []

        for i in range(4):
            for movie in movies[i]:
                if movie not in final_movies:
                    final_movies.append(movie)

        return final_movies