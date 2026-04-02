"""
PauliBot Views
==============
Handles both frontend HTML rendering and API endpoints.
"""

import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .logic import PauliBotLogic
from .models import ChatHistory, CustomUser, Conversation
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ChatHistorySerializer,
    ConversationSerializer
)

# Initialize bot logic engine
bot = PauliBotLogic()

# ==============================================================================
# FRONTEND VIEWS (HTML PAGES)
# ==============================================================================

@ensure_csrf_cookie
def landing_view(request):
    """
    Renders the landing page with login/register options.
    Redirects authenticated users mostly to chat, but allows access if explicitly requested.
    """
    if request.user.is_authenticated:
        return redirect('chat_view')
    return render(request, 'chatbot/landing.html')

@ensure_csrf_cookie
def register_page(request):
    """
    Renders registration page and handles form submission.
    """
    if request.user.is_authenticated:
        return redirect('chat_view')
        
    if request.method == 'POST':
        # Create a mutable copy of request.data for serializer
        data = request.POST.copy()
        serializer = UserRegistrationSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect('chat_view')
        else:
            # Pass errors to template
            error_msg = next(iter(serializer.errors.values()))[0]
            return render(request, 'chatbot/register.html', {'error': error_msg})
            
    return render(request, 'chatbot/register.html')

def login_page(request):
    """
    Handles login form submission from landing page.
    """
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        password = request.POST.get('password')
        
        user = authenticate(request, username=student_id, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('chat_view')
        else:
            return render(request, 'chatbot/landing.html', {'error': 'Invalid Student ID or password'})
            
    return redirect('landing')

def logout_page(request):
    """
    Logs out user and redirects to landing page.
    """
    logout(request)
    return redirect('landing')

@ensure_csrf_cookie
def chat_view(request):
    """
    Renders the main chat interface.
    - Authenticated: Loads chat history
    - Guest: Loads empty chat
    """
    context = {}
    
    # HYBRID ACCESS LOGIC
    if request.user.is_authenticated:
        # Load history for students
        context['chat_history'] = ChatHistory.objects.filter(user=request.user).order_by('timestamp')
    else:
        # No history for guests
        context['chat_history'] = []
        
    return render(request, 'chatbot/chat.html', context)

# ==============================================================================
# API ENDPOINTS (AJAX/JSON)
# ==============================================================================

@api_view(['POST'])
def register_user(request):
    """API Endpoint for registration (JSON)"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            'message': 'User registered successfully',
            'user_id': user.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    """API Endpoint for login (JSON)"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    """API Endpoint for logout (JSON)"""
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@login_required
def get_chat_history(request):
    """API Endpoint to get chat history (JSON)"""
    chat_history = ChatHistory.objects.filter(user=request.user)
    serializer = ChatHistorySerializer(chat_history, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
@login_required
def conversation_list(request):
    """
    List all conversations or create a new one.
    """
    if request.method == 'GET':
        conversations = Conversation.objects.filter(user=request.user, is_active=True).order_by('-updated_at')
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Create new conversation
        conversation = Conversation.objects.create(user=request.user)
        return Response({
            'message': 'Conversation created',
            'conversation_id': conversation.id,
            'title': conversation.title
        }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@login_required
def conversation_detail(request, conversation_id):
    """
    Get messages for a specific conversation or delete it.
    """
    try:
        conversation = Conversation.objects.get(id=conversation_id, user=request.user, is_active=True)
    except Conversation.DoesNotExist:
        return Response({'error': 'Conversation not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        messages = conversation.messages.all().order_by('timestamp')
        serializer = ChatHistorySerializer(messages, many=True)
        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        conversation.is_active = False  # Soft delete
        conversation.save()
        return Response({'message': 'Conversation deleted'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def chat_api(request):
    """
    Hybrid Access Chat Endpoint
    Handles actual logic for both Authenticated and Guest users.
    Supports Conversation History.
    """
    try:
        # Handle both JSON and Form data
        if request.content_type == 'application/json':
            data = request.data
        else:
            data = json.loads(request.body)
            
        user_message = data.get('message', '')
        conversation_id = data.get('conversation_id')
        
        if not user_message:
            return Response({'response': "Please type a message."}, status=400)

        # Process query with Logic Engine
        bot_response = bot.process_query(user_message)
        
        # HYBRID ACCESS: SAVE Logic
        if request.user.is_authenticated:
            # Student: Save to DB
            
            # Find or Create Conversation
            if conversation_id:
                try:
                    conversation = Conversation.objects.get(id=conversation_id, user=request.user, is_active=True)
                except Conversation.DoesNotExist:
                    # User sent an invalid ID, create a new one to be safe
                    conversation = Conversation.objects.create(user=request.user, title=user_message[:30] + "...")
            else:
                # Create new conversation if none provided
                # Use first message as title (truncated)
                title = user_message[:30] + "..." if len(user_message) > 30 else user_message
                conversation = Conversation.objects.create(user=request.user, title=title)
            
            # Update title if it's "New Chat" and this is the first real message
            if conversation.title == "New Chat":
                conversation.title = user_message[:30] + "..." if len(user_message) > 30 else user_message
                conversation.save()

            # Save Message
            chat_entry = ChatHistory.objects.create(
                user=request.user,
                conversation=conversation,
                message=user_message,
                response=bot_response
            )
            
            # Update conversation timestamp
            conversation.save()
            
            saved = True
            user_type = request.user.username
            active_conversation_id = conversation.id
            conversation_title = conversation.title
            chat_history_id = chat_entry.id
        else:
            # Guest: Do NOT Save
            saved = False
            user_type = 'guest'
            active_conversation_id = None
            conversation_title = None
            chat_history_id = None
            
        return Response({
            'response': bot_response,
            'saved': saved,
            'user': user_type,
            'conversation_id': active_conversation_id,
            'conversation_title': conversation_title,
            'chat_history_id': chat_history_id
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['PATCH'])
def submit_feedback(request, chat_id):
    """
    Submit feedback (thumbs up/down) for a specific chat response.
    Works for both authenticated users (own messages) and allows guest feedback.
    """
    try:
        chat_entry = ChatHistory.objects.get(id=chat_id)
        
        # Security: Only the owning user can give feedback on their messages
        if request.user.is_authenticated and chat_entry.user != request.user:
            return Response({'error': 'Unauthorized'}, status=403)
        
        feedback_value = request.data.get('feedback')
        if feedback_value not in ('positive', 'negative', None):
            return Response({'error': 'Invalid feedback value'}, status=400)
        
        chat_entry.feedback = feedback_value
        chat_entry.save(update_fields=['feedback'])
        
        return Response({
            'message': 'Feedback submitted',
            'chat_id': chat_id,
            'feedback': feedback_value
        })
        
    except ChatHistory.DoesNotExist:
        return Response({'error': 'Chat entry not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
