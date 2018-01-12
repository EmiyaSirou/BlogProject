from django.conf.urls import url
from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.article_detail, name = 'detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$',views.archives,name = 'archives'),
    url(r'^category/(?P<pk>[0-9a-zA-Z]+)/$', views.CategoryView.as_view(), name='category')
]