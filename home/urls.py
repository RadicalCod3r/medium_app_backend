from django.urls import path, include
from . import views
from home.views import CategoryListView, ArticleDetailView, ArticleListView



app_name = "home"


urlpatterns = [
	path('categories/', CategoryListView.as_view(), name='category-list'),
	path('articles/', ArticleListView.as_view(), name="article-list"),
	path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),

]
