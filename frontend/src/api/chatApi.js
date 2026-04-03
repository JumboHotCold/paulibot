/**
 * PauliBot Chat API Layer
 * =======================
 * Handles all communication with the Django REST Framework backend.
 * Uses fetch with credentials for session-based auth + CSRF protection.
 */

/**
 * Extract a cookie value by name from document.cookie.
 */
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    cookie = cookie.trim();
    if (cookie.startsWith(name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

/**
 * Ensure we have a CSRF token by hitting a Django endpoint that sets the cookie.
 * The Vite proxy forwards /api/* to Django, which returns the csrftoken cookie.
 */
export async function ensureCsrfToken() {
  if (!getCookie('csrftoken')) {
    try {
      // Hit any GET endpoint to receive the CSRF cookie
      await fetch('/api/conversations', {
        credentials: 'include',
      });
    } catch (e) {
      console.warn('Could not fetch CSRF token:', e);
    }
  }
}

/**
 * Send a message to PauliBot and receive the AI response.
 * 
 * @param {string} message - The user's message text
 * @param {number|null} conversationId - Optional conversation ID for history tracking
 * @returns {Promise<Object>} - { response, saved, user, conversation_id, conversation_title, chat_history_id }
 */
export async function sendMessage(message, conversationId = null) {
  const csrfToken = getCookie('csrftoken');

  const res = await fetch('/api/chat', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(csrfToken && { 'X-CSRFToken': csrfToken }),
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

/**
 * Fetch chat history for the logged-in user.
 */
export async function fetchConversations() {
  const res = await fetch('/api/conversations', {
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Failed to fetch conversations');
  return res.json();
}

/**
 * Fetch messages for a specific conversation.
 */
export async function fetchConversationDetails(id) {
  const res = await fetch(`/api/conversations/${id}`, {
    credentials: 'include',
  });
  if (!res.ok) throw new Error('Failed to fetch conversation details');
  return res.json();
}

/**
 * Create a new conversation explicitly.
 */
export async function createConversation() {
  const csrfToken = getCookie('csrftoken');
  const res = await fetch('/api/conversations', {
    method: 'POST',
    credentials: 'include',
    headers: {
      ...(csrfToken && { 'X-CSRFToken': csrfToken }),
    },
  });
  if (!res.ok) throw new Error('Failed to create conversation');
  return res.json();
}
