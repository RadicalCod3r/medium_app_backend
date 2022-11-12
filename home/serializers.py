from rest_framework import serializers
from .models import Category, Article

class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleDetailSerializer(ArticleListSerializer):

    class Meta:
        model = Article
        fields = '__all__'