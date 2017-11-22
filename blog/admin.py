from django.contrib import admin
from blog.models import Category,Tag,Article

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'creat_time', 'modified_time', 'category', 'author']

admin.site.register(Article,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)