from pyexpat import model
from django.db import models

# Create your models here.

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_url = models.CharField(max_length = 20)

