from users.models import User
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
def get_random_posts(request, author_id):
    random_posts = []

    user = User.objects.get(pk=author_id)
    user_posts = user.posts.all()

    pid_1, pid_2, pid_3 = random.sample(range(0, user_posts.count()), 3)

    for id, post in enumerate(user_posts):
        if id == pid_1 or id == pid_2 or id == pid_3:
            random_posts.append(post)

    serializer = PostListSerializer(random_posts, many=True)
    return Response(serializer.data)