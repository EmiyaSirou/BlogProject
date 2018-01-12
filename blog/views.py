from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.generic import ListView, DetailView

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
    article.increase_reading_quantity()
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


class IndexView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'
    paginate_by = 10


class CategoryView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)

        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_reading_quantity()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body,
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                      ])
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'comment_form': form,
            'comment_list': comment_list
        })
        return context