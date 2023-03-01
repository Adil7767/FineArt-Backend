from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .renderers import UserRenderer
from rest_framework.permissions import AllowAny


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(viewsets.ModelViewSet):
    http_method_names = ['post']
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
    serializer_class = UserProfileSerializer
    renderer_classes = [UserRenderer]

    def list(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = UserChangePasswordSerializer
    renderer_classes = [UserRenderer]

    def create(self, request):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.data.get('password')
            confirm_password = serializer.data.get('confirm_password')
            previous_password = serializer.data.get('previous_password')
            user0 = request.user
            user = authenticate(email=user0, password=previous_password)
            if user is not None:
                if password != confirm_password:
                    raise serializers.ValidationError("Password and Confirm Password Doesn't match.")
                user0.set_password(password)
                user0.save()
                return Response({'msg': 'Password Change Successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors': {'non_field_errors': ['Previous_Password is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendResetPasswordView(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = SendResetPasswordSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = SendResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg': 'Password Reset link send. Please check your Email.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(viewsets.ModelViewSet):
    http_method_names = ['post']
    serializer_class = UserPasswordResetSerializer
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = UserPasswordResetSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.data.get('otp')
            if User.objects.filter(otp=otp).exists():
                user = User.objects.get(otp=otp)
                password = serializer.data.get('password')
                confirm_password = serializer.data.get('confirm_password')
                if password != confirm_password:
                    raise serializers.ValidationError("Password and Confirm Password Doesn't match.")
                user.set_password(password)
                user.otp = None
                user.save()
                return Response({'msg': 'Password Change Successful'}, status=status.HTTP_200_OK)
            return Response({'errors': {'non_field_errors': ['OTP is not Valid']}}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)