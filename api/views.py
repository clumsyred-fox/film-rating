from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from api.serializers import ObtainTokenSerializer, RegistrationSerializer
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from api_yamdb.settings import FROM_EMAIL


class AuthTokenView(APIView):
    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            confirmation_code = serializer.data['confirmation_code']
            user = get_object_or_404(CustomUser, username=username)
            if confirmation_code != user.confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken.for_user(user)
            return Response(
                {'token': str(token.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            confirmation_code = default_token_generator.make_token(username)
            CustomUser.objects.create_user(
                username=username,
                email=email,
                confirmation_code=confirmation_code
            )
            send_mail(
                'Подтверждение регистрации на YAMDB',
                f'Код подтверждения: {confirmation_code}',
                from_email=FROM_EMAIL,
                recipient_list=(serializer.data['email'],),
                fail_silently=False,
            )
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
