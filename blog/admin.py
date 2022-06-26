from django.contrib import admin

# Register your models here.
from blog.models import Comment, Article, Category, ArticleCategory

admin.site.register(Comment)
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(ArticleCategory)