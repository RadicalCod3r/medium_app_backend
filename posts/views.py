from posts.serializers import PostDetailSerializer, PostListSerializer
from posts.models import Post
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.paginator import Paginator

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
