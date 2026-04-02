"""
PauliBot API Serializers
=========================
Author: Senior Full-Stack Developer & DevOps Engineer
Purpose: Django REST Framework serializers for API request/response validation

Serializers:
1. UserRegistrationSerializer - Validates new user registration
2. UserLoginSerializer - Validates login credentials
3. ChatHistorySerializer - Formats chat history for API responses
"""

from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser, ChatHistory, Conversation


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration endpoint.
    
    Validates student_id, username, password, and email.
    Password is write-only and automatically hashed by Django.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        help_text="Password (will be hashed automatically)"
    )
    
    class Meta:
        model = CustomUser
        fields = ['id', 'student_id', 'username', 'email', 'password', 'first_name', 'last_name']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        """
        Create new user with hashed password.
        
        Uses Django's create_user() method which automatically hashes
        the password using PBKDF2 algorithm.
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            student_id=validated_data['student_id'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login endpoint.
    
    Validates student_id and password against database.
    """
    student_id = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, data):
        """
        Validate credentials using Django's authenticate() method.
        
        This method checks the hashed password against the database.
        """
        student_id = data.get('student_id')
        password = data.get('password')
        
        if student_id and password:
            # We pass student_id as the 'username' parameter to authenticate()
            # because our custom backend StudentIDBackend expects it there.
            user = authenticate(username=student_id, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid Student ID or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'student_id' and 'password'.")
        
        return data


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for conversation list.
    """
    class Meta:
        model = Conversation
        fields = ['id', 'title', 'created_at', 'updated_at', 'is_active']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for chat history retrieval endpoint.
    
    Formats chat history with user details and timestamps.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    student_id = serializers.CharField(source='user.student_id', read_only=True)
    conversation_id = serializers.IntegerField(source='conversation.id', read_only=True, allow_null=True)
    
    class Meta:
        model = ChatHistory
        fields = ['id', 'username', 'student_id', 'conversation_id', 'message', 'response', 'feedback', 'timestamp']
        read_only_fields = ['id', 'username', 'student_id', 'timestamp', 'conversation_id']
