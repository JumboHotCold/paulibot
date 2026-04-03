import { useRef, useEffect } from 'react';

// Parses an incoming message to separate true text from structured suggestions.
// Example: "Kamusta? [SUGGESTIONS: 'Hi' | 'Hello']"
function parseMessage(rawText) {
  if (!rawText) return { text: '', suggestions: [] };
  
  const regex = /\[SUGGESTIONS:\s*(.*?)\]/g;
  let suggestions = [];
  let cleanText = rawText;

  const match = regex.exec(rawText);
  if (match && match[1]) {
    // split by |
    const rawSuggestions = match[1].split('|');
    // strip out wrapping quotes and trim whitespace
    suggestions = rawSuggestions
      .map(s => s.replace(/^["'\s]+|["'\s]+$/g, ''))
      .filter(Boolean);
    
    // remove the suggestion block from the display text
    cleanText = rawText.replace(match[0], '').trim();
  }
  return { text: cleanText, suggestions };
}

export default function Dashboard({ user, onLogout, onNavigateLogin, messages, isTyping, onSend, onNewChat, conversations = [] }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const isGuest = user.type === 'GUEST';
  const isChatEmpty = messages.length === 0;
  const initial = user?.name ? user.name.charAt(0).toUpperCase() : 'S';

  const handleSend = (e) => {
    e.preventDefault();
    const inputEl = e.target.elements.message;
    const text = inputEl.value.trim();
    if (!text || isTyping) return;
    onSend(text);
    inputEl.value = '';
  };

  return (
    <div className="chat-layout">
      
      {/* Sidebar - Exact replica of chat.html <aside class="sidebar"> */}
      {!isGuest && (
        <aside className="sidebar">
          <div className="sidebar-header">
            <button className="new-chat-btn" onClick={onNewChat}>
              <span>+</span> New Chat
            </button>
          </div>

          <div className="sidebar-content">
            {conversations.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '20px', color: '#999' }}>
                No previous conversations
              </div>
            ) : (
              conversations.map(conv => (
                <button key={conv.id} className="conversation-item">
                  {conv.title || "New Chat"}
                </button>
              ))
            )}
          </div>

          <div className="sidebar-footer">
            <div className="user-profile">
              <div className="avatar">{initial}</div>
              <div className="user-info">
                <div>{user.name}</div>
                <span>{user.id}</span>
              </div>
            </div>
            <button className="logout-btn" onClick={onLogout}>Log Out</button>
          </div>
        </aside>
      )}

      {/* Main Chat - Exact replica of <main class="main-chat"> */}
      <main className="main-chat">
        
        <header className="chat-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <div className="chat-title">
              {!isGuest ? 'New Chat' : 'Welcome Guest'}
            </div>
          </div>
          {isGuest && (
            <div>
              <button 
                onClick={onNavigateLogin} 
                style={{ background: 'none', border: 'none', color: '#0A4D2E', fontWeight: 600, cursor: 'pointer', fontSize: '1em' }}
              >
                Login
              </button>
            </div>
          )}
        </header>

        <div className="messages-container">
          {isChatEmpty ? (
            <div className="empty-state">
              <img 
                src="/spus-logo.webp" 
                alt="SPUS Logo" 
                style={{ height: '100px', width: '100px', objectFit: 'contain', marginBottom: '20px', filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.2))' }}
              />
              <h1>PauliBot</h1>
              <p>Saint Paul University Surigao AI Assistant</p>
              {isGuest && (
                <p style={{ marginTop: '10px', color: '#D4AF37', fontWeight: 600 }}>⚠️ Guest Mode: Chat history not saved</p>
              )}

              <div className="suggestions">
                {[
                  "What courses are available?",
                  "How do I enroll?",
                  "Where is the registrar office?",
                  "School calendar activities"
                ].map((prompt, i) => (
                  <div key={i} className="suggestion-card" onClick={() => { if (!isTyping) onSend(prompt); }}>
                    {prompt}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            <>
              {messages.map((msg, idx) => {
                const { text, suggestions } = msg.isUser ? { text: msg.text, suggestions: [] } : parseMessage(msg.text);

                return (
                  <div key={idx} className={`message-wrapper ${msg.isUser ? 'user' : 'bot'}`}>
                    <div className="message-avatar">
                      {msg.isUser ? initial : 'P'}
                    </div>
                    <div className="message-content">
                      {text}
                      
                      {suggestions.length > 0 && (
                        <div className="follow-up-chips">
                          {suggestions.map((s, i) => (
                            <button 
                              key={i} 
                              className="follow-up-chip" 
                              onClick={() => { if (!isTyping) onSend(s); }}
                            >
                              {s}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}

              {isTyping && (
                <div className="message-wrapper bot">
                  <div className="message-avatar">P</div>
                  <div className="message-content" style={{ padding: '0' }}>
                    <div className="typing-indicator">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} style={{ height: '2px' }}></div>
            </>
          )}
        </div>

        {/* Input Area - Exact replica of chat.html input area */}
        <div className="input-area">
          <form className="input-wrapper" onSubmit={handleSend}>
            <input 
              type="text" 
              name="message"
              className="chat-input" 
              placeholder="Type your question here..." 
              autoComplete="off" 
              disabled={isTyping}
            />
            <button type="submit" className="send-btn" disabled={isTyping}>
              <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"></path>
              </svg>
            </button>
          </form>
        </div>

      </main>
    </div>
  );
}
