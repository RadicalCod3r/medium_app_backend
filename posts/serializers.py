from rest_framework import serializers
from .models import Category, Post
from users.models import User
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'caption', 'image', 'slug', 'created_at', 'updated_at', 'read_time', 'writer', 'category']

    def get_writer(self, obj):
        serializer = UserSerializer(obj.writer, many=False)
        return serializer.data

    def get_category(self, obj):
        serializer = CategorySerializer(obj.category, many=False)
        return serializer.data        

class PostDetailSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField(read_only=True)
    category = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_writer(self, obj):
        serializer = UserSerializer(obj.writer, many=False)
        return serializer.data

    def get_category(self, obj):
        serializer = CategorySerializer(obj.category, many=False)
        return serializer.data