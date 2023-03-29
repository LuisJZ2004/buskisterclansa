import collections

from django.db import models
from django.utils.text import slugify

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
    
    def get_movie_years(self) -> tuple:
        return tuple(collections.Counter(
            [str(movie.year.year) for movie in self.as_producer.all()]
        ).keys())
    
    def get_movies_sorted_by_year(self):
        years = self.get_movie_years()
        movies_by_years = {}

        for year in years:
            movies_by_years[year] = self.as_producer.filter(year__year=year)

        return movies_by_years