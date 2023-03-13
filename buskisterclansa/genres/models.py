from django.db import models
from django.utils.text import slugify

class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=False, null=False)
    slug = models.SlugField(max_length=50, blank=False, default=None, editable=False)
    
    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        self.name = self.name.capitalize()
        self.slug = slugify(self.name)

        return super().save(*args, **kwargs)