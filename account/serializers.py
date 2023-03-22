from rest_framework import serializers
from .models import *
from django.core.mail import send_mail
import random


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone_number', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('confirm_password')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password Doesn't match.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'gender', 'phone_number']


class UserChangePasswordSerializer(serializers.ModelSerializer):
    previous_password = serializers.CharField(max_length=255, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['previous_password', 'password', 'confirm_password']


class SendResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            otp = random_with_N_digits(6)
            user.otp = otp
            user.save()
            msg = 'Your 6 Digit Verification Pin: {}'.format(otp)
            send_mail(
                'Reset Your Password',
                msg,
                'shahzadkulachi08@gmail.com',
                [user.email],
                fail_silently=False,
            )
            return attrs
        else:
            raise serializers.ValidationError('You are not Registered User')


class UserPasswordResetSerializer(serializers.ModelSerializer):
    otp = serializers.IntegerField()
    confirm_password = serializers.CharField(max_length=255, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['otp', 'password', 'confirm_password']
