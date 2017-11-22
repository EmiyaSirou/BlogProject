from blog.models import Category,Tag,Article
from django.utils import timezone
from django.contrib.auth.models import User

c = Category(name='category test')
c.save()
t = Tag(name='tag test')
t.save()

# user = User.objects.get(username='emiya')
# c = Category.objects.get(name='category test')
#
# p = Article(title='title test', body='body test', created_time=timezone.now(), modified_time=timezone.now(), category=c, author=user)
# p.save()
#
# print(Category.objects.all())
# print(Tag.objects.all())
# print(Article.objects.all())
# print(User.objects.all())


