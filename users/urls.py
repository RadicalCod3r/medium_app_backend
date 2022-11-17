from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', views.user_profile, name='user_profile'),
    path('list/', views.list_users, name='users_list'),
]