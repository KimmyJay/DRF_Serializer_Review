from django.urls import path
from blog import views

urlpatterns = [
    path('article/', views.ArticleView.as_view()),
    path('article/<int:id>', views.ArticleView.as_view()),
    # path('comment/', views.CommentView.as_view()),

]