"""
PauliBot Database Models
========================
Author: Senior Full-Stack Developer & DevOps Engineer
Purpose: Define database schema for user authentication and chat history storage

Models:
1. CustomUser - Extends Django's AbstractUser with student_id field
2. ChatHistory - Stores chat conversations linked to authenticated users
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom User model for PauliBot authentication.
    
    Extends Django's AbstractUser to include student ID field.
    Passwords are automatically hashed by Django's authentication system.
    
    Fields:
        student_id: Unique identifier for students (e.g., "2024-00001")
        username: Login username (inherited from AbstractUser)
        password: Hashed password using PBKDF2 (inherited from AbstractUser)
        email: Student email address (inherited from AbstractUser)
        first_name: Student first name (inherited from AbstractUser)
        last_name: Student last name (inherited from AbstractUser)
    """
    student_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Student ID number (e.g., 2024-00001)"
    )
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.student_id} - {self.username}"


class Conversation(models.Model):
    """
    Conversation grouping model.
    
    Groups multiple ChatHistory messages into a distinct session/thread.
    Allows for sidebar navigation similar to ChatGPT.
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='conversations',
        help_text="The user who owns this conversation"
    )
    title = models.CharField(
        max_length=255,
        default="New Chat",
        help_text="Title of the conversation (auto-generated or user-set)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class ChatHistory(models.Model):
    """
    Chat history model for authenticated users.
    
    Stores conversation between students and PauliBot.
    Guest users do NOT have chat history saved (transient sessions).
    
    Fields:
        user: Foreign key to CustomUser (CASCADE delete)
        conversation: Link to parent Conversation (optional for now)
        message: User's input message
        response: Bot's generated response
        timestamp: Auto-generated timestamp for conversation ordering
    """
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='chat_history',
        help_text="The authenticated user who sent this message"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True,
        help_text="The conversation thread this message belongs to"
    )
    message = models.TextField(
        help_text="User's input message/question"
    )
    response = models.TextField(
        help_text="Bot's generated response"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When this chat exchange occurred"
    )
    
    class Meta:
        verbose_name = "Chat History"
        verbose_name_plural = "Chat Histories"
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['conversation', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
