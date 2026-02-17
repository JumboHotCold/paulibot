# 🎉 PauliBot 2.0 - SPUS Edition

## 🎨 New UI & Features (Completed)

We have successfully overhauled the UI to match **Saint Paul University Surigao** branding and implemented **Persistent Conversation History**.

### 1. Visual Redesign
*   **Colors**: Paulinian Green (`#0A4D2E`) and Gold (`#D4AF37`).
*   **Typography**: 'Merriweather' (Serif) for headings, 'Inter' (Sans) for body.
*   **Modern Layout**: Split-screen landing page, floating input labels, and card-based design.

### 2. Conversation History (Like ChatGPT)
*   **Sidebar**: A left-hand panel listing previous conversations.
*   **Auto-Titling**: New chats are automatically named based on the first message.
*   **Conversation Management**: Structure data into "Threads" rather than a single flat history.
*   **Delete Chat**: Option to remove old conversations.

---

## 🧪 How to Test

### 1. View the Redesign
Open: **[http://localhost:8000](http://localhost:8000)**
*   Verify the **Green/Gold theme**.
*   Check the "Visitor Access" vs "Student Portal" split.

### 2. Test Conversation History (Student Mode)
1.  **Login** as a student.
2.  You should see the **Sidebar** on the left.
3.  **Start a Chat**: Type "Hello World".
4.  **Check Sidebar**: A new item "Hello World..." should appear in the sidebar.
5.  **New Chat**: Click the **"+ New Chat"** button. The main area clears.
6.  **Switch Chats**: Click on the previous chat in the sidebar. The messages should reload.

### 3. Test Guest Mode
1.  **Logout** and click **"Continue as Guest"**.
2.  **Verify**: The Sidebar should be **HIDDEN**.
3.  Send a message. Refresh the page.
4.  **Verify**: The chat history is GONE (Transient session).

---

## 🛠️ Technical Implementation for Thesis

### Database Schema
We added a `Conversation` model to group messages:
```python
class Conversation(models.Model):
    user = ForeignKey(CustomUser)
    title = CharField()
    # ...
```
And updated `ChatHistory` to link to it.

### API Endpoints
*   `GET /api/conversations`: List sidebar items.
*   `GET /api/conversations/<id>`: Load messages for a chat.
*   `POST /api/chat`: Now accepts `conversation_id` to thread messages.

### Frontend Logic
*   **Pure AJAX**: No page reloads when switching chats.
*   **State Management**: `currentConversationId` tracks the active thread in JavaScript.

**Ready for Defense Demo!** 🚀
