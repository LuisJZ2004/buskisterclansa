from django.db import models
from django.utils.text import slugify

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