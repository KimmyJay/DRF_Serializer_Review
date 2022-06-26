from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from blog.models import Article, Comment, Category
from blog.serializers import ArticleSerializer

from django.db.models import Q
from django.utils import timezone

from datetime import timedelta

class ArticleView(APIView):
    # get logged-in user's articles
    # 
    def get(self, request):
        user = request.user
        hour_ago = timezone.now()-timedelta(hours=1)
        
        query = Q()
        query.add(Q(author=user), Q.AND)
        query.add(Q(exposure_start_date__gte=hour_ago), Q.AND)
 
        # get current user's articles that were posted less than an hour ago
        my_articles = Article.objects.filter(query)
        article_serializer = ArticleSerializer(my_articles, many=True, context={"request": request})

        return Response(article_serializer.data, status=status.HTTP_200_OK)

    # write a new article
    def post(self, request):
        # assign current user as author
        user = request.user
        request.data['author'] = user.id
        categories = request.data.get('categories', [])
        
        context={
            "request": request,
            "categories": categories
        }

        article_serializer = ArticleSerializer(data=request.data, context=context)
        article_serializer.is_valid(raise_exception=True)
        article_serializer.save()

        return Response(article_serializer.data, status=status.HTTP_200_OK)

    # edit an article
    def put(self, request, id):
        article = Article.objects.get(id=id)
        categories = request.data.get('categories', [])
        
        context={
            "request": request,
            "categories": categories
        }
       
        # set partial=True to indicate we are editing only some fields 
        article_serializer = ArticleSerializer(article, data=request.data, partial=True, context=context)
        article_serializer.is_valid(raise_exception=True)
        article_serializer.save()
        return Response(article_serializer.data, status=status.HTTP_200_OK)
    

    # delete an aritcle
    def delete(self, request, id):
        article = Article.objects.get(id=id)
        article.delete()
        return Response({"message": "Article Removed"})



