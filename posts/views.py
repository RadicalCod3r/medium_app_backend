from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.models import Post
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
import random
# Create your views here.
@api_view(['GET',])
def list_posts(request):
    posts = Post.objects.all()
    page_number = request.GET.get('page')

    if page_number:
        paginator = Paginator(posts, 6)
        page_obj = paginator.page(int(page_number))

        serializer = PostListSerializer(page_obj, many=True)
        return Response({ 'data': serializer.data, 'count': len(posts) })
    else:
        serializer = PostListSerializer(posts, many=True)
        return Response({'data': serializer.data, 'count': len(posts)})

@api_view(['GET',])
def list_trending_posts(request):
    posts = Post.objects.all().order_by('-created_at')[:6]
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET',])
def post_detail(request, id):
    try:
        post = Post.objects.get(pk=id)
        serializer = PostDetailSerializer(post, many=False)
        return Response(serializer.data)
    except:
        return Response({'detail': 'error finding the post'})

@api_view(['GET',])
def get_random_posts(request, id):
    random_post = None
    post_count = Post.objects.all().count() + 1
    while not Post.objects.get().filter(id=random_post).exists():
        for obj in range(post_count):
            author = random.randint(0, post_count)
            if Post.objects.all().filter(id=author).exists():
                random_post=author
                return random_post
    serializer = PostListSerializer(random_post, many=False)
    return Response(serializer.data)
