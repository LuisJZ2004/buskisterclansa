# Django
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

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

    def is_staff(self, job_model: models.Model):
        """
        Returns if this staff has one or more of the movie_staff jobs (director, script etc.). The staff model
        must be sended to make the query (Director, Cast, Producer etc.)
        """
        try:
            job_model.objects.get(movie_staff__pk=self.pk)
            return True
        except MultipleObjectsReturned:
            return True
        except ObjectDoesNotExist: 
            return False