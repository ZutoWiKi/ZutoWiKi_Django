from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Work(models.Model):
    NOVEL       = 0
    POEM        = 1
    MUSIC       = 2
    GAME        = 3
    MOVIE       = 4
    PERFORMANCE = 5
    ANIMATION   = 6

    TYPE_CHOICES = [
        (NOVEL,       "novel"),
        (POEM,        "poem"),
        (MUSIC,       "music"),
        (GAME,        "game"),
        (MOVIE,       "movie"),
        (PERFORMANCE, "performance"),
        (ANIMATION,   "animation"),
    ]
    type_index  = models.IntegerField(choices=TYPE_CHOICES)
    title       = models.CharField(max_length=100)
    author      = models.CharField(max_length=100)
    cover_image = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.get_type_index_display()}] {self.title}"
    
class Write(models.Model):
    