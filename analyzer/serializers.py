from dataclasses import fields
from rest_framework import serializers
from .models import Resume
from django.contrib.auth.models import User

class ResumeSerializer(serializers.ModelSerializer):
  class Meta:
    model = Resume
    fields= '__all__'
    read_only_fields=['user', 'uploaded_at']

class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)
  class Meta:
    model = User
    fields = ['username', 'email', 'password']
  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password']
    )
    return user
