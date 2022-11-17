from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'accounts'
urlpatterns = [
	path('register/', views.UserRegisterView.as_view(), name='user_register'),
	path('verify/', views.UserRegisterVerifyCodeView.as_view(), name='verify_code'),
    #path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('logout/', views.LogoutView.as_view(), name='logout'),

]