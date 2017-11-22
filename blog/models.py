from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#分类
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

#标签
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

#正文
class Article(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    creat_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title + "\n" + self.body + "\n"

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})