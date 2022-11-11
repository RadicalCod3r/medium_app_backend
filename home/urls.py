from django.urls import path, include
from . import views

app_name = "home"


urlpatterns = [
	path('posts/', views.post_page_list, name="post-list"),
]