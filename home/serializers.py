from rest_framework import serializers
from .models import Category, Article
from accounts.serializers import UserSerializer


class ArticleListSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'body', 'image', 'updated_at', 'author', 'categories']

    def get_author(self, obj):
        serializer = UserSerializer(obj.author, many=False)
        return serializer.data

    def get_categories(self, obj):
        serializer = CategorySerializer(obj.categories, many=False)
        return serializer.data        



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleDetailSerializer(ArticleListSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    categories = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = '__all__'

    def get_author(self, obj):
        serializer = UserSerializer(obj.author, many=False)
        return serializer.data

    def get_categories(self, obj):
        serializer = CategorySerializer(obj.categories, many=False)
        return serializer.data
