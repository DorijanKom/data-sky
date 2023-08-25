from rest_framework import serializers

from services.core.models import User


class UserAuthenticationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = ('id', 'email', 'is_staff', 'is_login_blocked', 'is_deleted')
        read_only_fields = fields