from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
from .serializers import UserSerializer, VerificationSerializer, PasswordResetSerializer




@api_view(['POST'])
@csrf_exempt
def api_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.is_active = False
        user.save()
        request.session['verification_code'] = random.randint(100000, 999999)
        email = EmailMessage(
            'Verify your email address',
            f'Your verification code is: {request.session["verification_code"]}',
            'noreply@example.com',
            [user.email],
            reply_to=[f'{request.scheme}://{request.get_host()}{reverse("api_verify_email")}?email={user.email}']
        )
        email.send()
        return Response({'success': True})
    else:
        errors = serializer.errors
        return Response({'success': False, 'errors': errors})

@api_view(['POST'])
@csrf_exempt
def api_verify_email(request):
    serializer = VerificationSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        verification_code = serializer.validated_data['verification_code']
        user = get_object_or_404(User, email=email)
        if verification_code == request.session.get('verification_code'):
            user.is_active = True
            user.save()
            return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
@csrf_exempt
def api_password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        request.session['verification_code'] = random.randint(100000, 999999)
        email = EmailMessage(
            'Reset your password',
            f'Your verification code is: {request.session["verification_code"]}',
            'noreply@example.com',
            [user.email],
            reply_to=[f'{request.scheme}://{request.get_host()}{reverse("api_password_reset_confirm")}?email={email}']
        )
        email.send()
        return Response({'success': True})
    return Response({'success': False})

@api_view(['POST'])
@csrf_exempt
def api_password_reset_confirm(request):
    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        user = get_object_or_404(User, email=email)
        verification_code = serializer.validated_data['verification_code']
        if verification_code == request.session.get('verification_code'):
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            return Response({'success': True})
    return Response({'success': False})
