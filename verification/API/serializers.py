from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class VerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.IntegerField()

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    verification_code = serializers.IntegerField()
