from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Article, Category
from .serializers import ArticleListSerializer,ArticleDetailSerializer, CategorySerializer
# Create your views here.


class CategoryListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ArticleListView(ListAPIView):
    queryset = Article.objects.filter()
    serializer_class = ArticleListSerializer
    filterset_fields = ['author']
    search_fields = ['title', 'description']


class ArticleDetailView(RetrieveAPIView):
    queryset = Article.objects.filter()
    serializer_class = ArticleDetailSerializer