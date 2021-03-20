from django.db import models


class Problem(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    length = models.PositiveSmallIntegerField()
    consonant = models.CharField(max_length=10)
    word = models.CharField(max_length=10)
    meaning = models.CharField(max_length=60)
