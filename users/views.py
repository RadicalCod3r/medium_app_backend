from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from .models import User

# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET',])
@permission_classes([permissions.IsAuthenticated,])
def user_profile(request):
    user = request.user
    try:
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except:
        return Response({'message': 'something is wrong!', 'status': status.HTTP_400_BAD_REQUEST})


@api_view(['GET',])
@permission_classes([permissions.IsAdminUser,])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)





class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
