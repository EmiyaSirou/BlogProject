from django.shortcuts import render, get_object_or_404, get_list_or_404
from blog.models import Article, Category
from comments.forms import CommentForm
from django.http import HttpResponse
import markdown


def index(request):
    article_list = Article.objects.all().order_by('-creat_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                     ])
    comment_form = CommentForm()
    comment_list = article.comment_set.all()
    context = {'article': article, 'comment_form': comment_form, 'comment_list': comment_list}

    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    article_list = Article.objects.filter(creat_time__year=year,
                                          creat_time__month=month).order_by('-creat_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})


def category(request, pk):
    # category = Category.objects.get(pk=pk)
    category = get_object_or_404(Category, pk=pk)
    # article_list = get_list_or_404(Article, category=tmp)
    article_list = Article.objects.filter(category=category).order_by('-creat_time')
    return render(request, 'blog/index.html', context={'article_list': article_list})
