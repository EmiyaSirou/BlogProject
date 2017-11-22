from blog.models import Article,Category
from django import template

register = template.Library()

@register.simple_tag
def get_recent_articles(num=5):
    return Article.objects.all().order_by('-creat_time')[:num]

@register.simple_tag
def archives():
    return Article.objects.dates('creat_time', 'month', order='DESC')

@register.simple_tag
def get_category():
    return Category.objects.all()