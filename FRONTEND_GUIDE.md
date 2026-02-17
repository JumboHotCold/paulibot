# 🎨 PauliBot Frontend Guide

You now have a complete, modern frontend interface for PauliBot! 

## 🚀 How to Access

**Open your browser to:** [http://localhost:8000](http://localhost:8000)

---

## 📱 Features Implemented

### 1. Landing Page (`/`)
- **Modern Design**: Gradient background with clean cards.
- **Login Form**: Standard username/password authentication.
- **Register Button**: Links to the registration page.
- **Guest Access**: prominent "Continue as Guest" button.

### 2. Registration Page (`/register/`)
- **Full Form**: Collects Student ID, Name, Email, Username, Password.
- **Auto-Login**: Automatically logs you in after successful registration.
- **Validation**: Checks for duplicate users or mismatched passwords.

### 3. Chat Interface (`/chat/`)
- **Hybrid Logic**:
  - **Students**: Sees "Student ID: [ID]" in header. Chat history is LOADED from database. New messages are SAVED.
  - **Guests**: Sees "Guest User" in header. Chat history is EMPTY. New messages are NOT SAVED.
- **Real-time**: AJAX-powered messaging (no page reloads).
- **Logout**: Button available in the header.

---

## 🛠️ Technical Details (For Your Thesis)

### Hybrid Access Logic
The core logic resides in `views.py`.

**View: `chat_view`**
```python
def chat_view(request):
    if request.user.is_authenticated:
        # Load history ONLY for authenticated users
        history = ChatHistory.objects.filter(user=request.user)
    else:
        # Empty list for guests
        history = []
    return render(request, 'chat.html', {'chat_history': history})
```

**API: `chat_api`**
```python
def chat_api(request):
    # ... process bot response ...
    
    if request.user.is_authenticated:
        # SAVE to Database
        ChatHistory.objects.create(user=request.user, ...)
        return Response({'saved': True})
    else:
        # DO NOT SAVE
        return Response({'saved': False})
```

### Guest Mode Security
- Guest chats are **never** written to the database.
- They exist only in the browser's current specific page view.
- Refreshing the page clears the guest chat (Privacy Feature).

---

## 🧪 How to Test

1. **Guest Mode**:
   - Go to [http://localhost:8000](http://localhost:8000)
   - Click **"Continue as Guest"**
   - Chat with the bot.
   - **Verify**: Refresh the page. The chat should disappear.

2. **Student Mode**:
   - Go to [http://localhost:8000](http://localhost:8000)
   - Click **"Create New Account"**
   - Register a new user.
   - Chat with the bot.
   - **Verify**: Refresh the page. The chat history PRESERVED.
   - **Verify**: Logout and Login again. The history is RELOADED.

## 📁 Key Files Created
- `chatbot/templates/chatbot/landing.html`
- `chatbot/templates/chatbot/register.html`
- `chatbot/templates/chatbot/chat.html`
- `chatbot/views.py` (Updated with page views)
- `chatbot/urls.py` (Updated with page routes)

**Enjoy your new PauliBot interface!** 🎉
