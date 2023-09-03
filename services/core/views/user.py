from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from services.core.constants.error import WRONG_CREDENTIALS, TOKEN_MISSING
from services.core.models import Directory
from services.core.models.user import User
from services.core.serializers.user import UserAuthenticationSerializer, UserSerializer
from services.core.utils.error_handler import error_response_from_code
from services.core.utils.wrapper_exception import WrapperException


class RegisterUserView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data.get('email'))

        user = User.objects.create_user(email=serializer.validated_data.get('email'),
                                        password=serializer.validated_data.get('password'),
                                        is_active=True)
        Directory.objects.create(
            name='/',
            user=user
        )

        return Response(status=status.HTTP_200_OK)


class LoginUserView(GenericAPIView):
    serializer_class = UserAuthenticationSerializer
    authentication_classes = []

    # def get(self, request, *args, **kwargs):
    #     token = request.META.get("HTTP_AUTHORIZATION")
    #
    #     if token:
    #         auth_user = CustomAuthentication().authenticate(request)
    #         data = UserSerializer(auth_user[0]).data
    #
    #         return Response(data, status=status.HTTP_200_OK)
    #     return error_response_from_code(TOKEN_MISSING)

    def post(self, request, *args, **kwargs):
        serializer = UserAuthenticationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(request, username=serializer.validated_data["email"],
                            password=serializer.validated_data["password"])

        if user is not None:
            login(request, user)
            return Response(data={'token': "Login successful"}, status=status.HTTP_200_OK)

        else:
            raise WrapperException(WRONG_CREDENTIALS)


class LogoutUserView(GenericAPIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)