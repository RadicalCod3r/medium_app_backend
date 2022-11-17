from rest_framework.generics import ListAPIView
from .models import Article, Category
from .serializers import ArticleListSerializer,ArticleDetailSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

@api_view(['GET',])
def list_trending_articles(request):
    articles = Article.objects.all().order_by('-created_at')
    serializer = ArticleListSerializer(articles, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def article_detail(request, id):
    try:
        article = Article.objects.get(pk=id)
        serializer = ArticleDetailSerializer(article, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': 'error finding the post'})








#class ArticleListView(ListAPIView):
 #   queryset = Article.objects.filter()
  #  serializer_class = ArticleListSerializer
   # filterset_fields = ['author']
    #search_fields = ['title', 'description']


#class ArticleDetailView(RetrieveAPIView):
#    queryset = Article.objects.filter()
#    serializer_class = ArticleDetailSerializer