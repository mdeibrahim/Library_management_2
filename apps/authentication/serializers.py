from rest_framework import serializers
from apps.member.models import Member
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import random

User= get_user_model()


class UserCreateSerializer(DjoserUserCreateSerializer): 
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email', 'password','confirm_password', 'role']
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True, 'min_length': 8},
            'confirm_password': {'write_only': True, 'min_length': 8}
        }
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        role = validated_data.pop('role', 'member')  # Default to 'member' if not provided
        user = User.objects.create_user(
            password=password,
            role=role,
            **validated_data
        )
        return user
    