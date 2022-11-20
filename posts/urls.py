from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list_posts, name='posts_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
    path('list/trending/', views.list_trending_posts, name='list_trending'),
    path('random-posts-by-authorid/<int:author_id>/', views.get_random_posts, name='random_three_posts'),
]