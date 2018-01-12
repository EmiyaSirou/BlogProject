import markdown
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 标签
class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


# 正文
class Article(models.Model):
    title = models.CharField(max_length=30)
    body = models.TextField()
    creat_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    excerpt = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    reading_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title + "\n" + self.body + "\n"

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_reading_quantity(self):
        self.reading_quantity += 1
        self.save(update_fields=['reading_quantity'])

    def save(self, *args, **kwargs):
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Article, self).save(*args, **kwargs)
