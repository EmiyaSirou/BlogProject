from django.db import models
from blog.models import Article


# Create your models here.

class Comment(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, blank=True)
    url = models.URLField(blank=True)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey(Article)

    def __str__(self):
        return self.text[:20]
