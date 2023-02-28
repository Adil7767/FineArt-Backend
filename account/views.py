from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRenderer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Registration Successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    renderer_classes = [UserRenderer]

    def list(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Change Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = SendResetPasswordSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        serializer = SendResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset link send. Please check your Email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(viewsets.ModelViewSet):
    http_method_names = ['post']
    queryset = User.objects.all()
    serializer_class = UserPasswordResetSerializer
    renderer_classes = [UserRenderer]

    def create(self, request, uid, token):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset Successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)