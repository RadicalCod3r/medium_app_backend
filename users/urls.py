from django.urls import path
from . import views

urlpatterns = [
    #path('login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('validate_phone/', views.verify_phone_send_otp_code, name='validate-phone'),
    path('validate_otp/', views.verify_otp, name='validate-otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('list/', views.list_users, name='users_list'),
]