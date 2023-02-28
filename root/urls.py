from django.urls import path, include
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from rest_framework.routers import DefaultRouter
from account.views import *

router = DefaultRouter()

router.register('register', UserRegistrationView, basename='register')
router.register('login', UserLoginView, basename='login')
router.register('profile', UserProfileView, basename='profile')
router.register('change-password', UserChangePasswordView, basename='change-password')
router.register('send-reset-password-email', SendResetPasswordView, basename='send-password')
router.register('reset-password/<uid>/<token>', UserPasswordResetView, basename='reset-password')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

    path('openapi', get_schema_view(
        title="Your Project",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),

    path('', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),

]
