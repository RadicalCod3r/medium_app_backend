from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User



class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'title', 'description', 'name']
    

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name





class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'title', 'description', 'token', 'image']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)