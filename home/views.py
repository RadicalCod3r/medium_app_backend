from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer
# Create your views here.

@api_view(['GET'])
def post_page_list(request):
    posts = Article.objects.all()
    serializer = ArticleSerializer(posts, many=True)
    return Response(serializer.data)