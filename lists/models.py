from django.db import models

# Create your models here.

class ItemModel(models.Model):
    text = models.TextField()