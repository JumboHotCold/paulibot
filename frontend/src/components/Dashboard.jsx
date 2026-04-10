import { useRef, useEffect, useState } from 'react';
import ThemeToggle from './ThemeToggle';
import EditProfileModal from './EditProfileModal';
import { fetchAnnouncements } from '../api/chatApi';

// =============================================================================
// SUB-COMPONENTS FOR Markdown & Sources
// =============================================================================

function CheckboxLine({ text, indent }) {
  const [checked, setChecked] = useState(false);
  return (
    <label style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', cursor: 'pointer', marginLeft: indent.length * 8 + 'px', opacity: checked ? 0.6 : 1, textDecoration: checked ? 'line-through' : 'none', marginBottom: '6px' }}>
      <input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} style={{ marginTop: '5px', accentColor: 'var(--spus-green)' }} />
      <span style={{ flex: 1 }}>{text}</span>
    </label>
  );
}

function MarkdownRenderer({ text }) {
  return (
    <div className="markdown-renderer">
      {text.split('\n').map((line, idx) => {
        const listRegex = /^(\s*)(?:-\s|\*\s|\d+\.\s)(.*)$/;
        const match = line.match(listRegex);
        if (match) {
          return <CheckboxLine key={idx} text={match[2]} indent={match[1]} />;
        }
        return line.trim() ? <p key={idx} style={{ marginBottom: '8px' }}>{line}</p> : <div key={idx} style={{ height: '8px' }} />;
      })}
    </div>
  );
}

function SourcesAccordion({ sources }) {
  const [open, setOpen] = useState(false);
  if (!sources || sources.length === 0) return null;
  return (
    <div className="sources-container" style={{ marginTop: '12px', fontSize: '0.86em', borderTop: '1px solid rgba(0,0,0,0.06)', paddingTop: '8px' }}>
      <button onClick={() => setOpen(!open)} style={{ background: 'none', border: 'none', color: 'var(--text-light)', cursor: 'pointer', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '6px', padding: '4px 0' }}>
        📎 Sources {open ? '▼' : '▶'}
      </button>
      {open && (
        <div style={{ marginTop: '8px', padding: '10px 14px', background: 'rgba(0,0,0,0.03)', borderRadius: '8px', color: 'var(--text-dark)' }}>
          {sources.map((s, i) => (
            <div key={i} style={{ marginBottom: '6px', display: 'flex', gap: '6px', alignItems: 'flex-start' }}>
              <span>📄</span>
              <span style={{ lineHeight: 1.4 }}>
                {s.url ? <a href={s.url} target="_blank" rel="noreferrer" style={{color: 'var(--spus-green)', textDecoration: 'underline', fontWeight: 500}}>{s.title}</a> : s.title}
                {s.page ? ` (Page ${s.page})` : ''}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

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

export default function Dashboard({ user, onLogout, onNavigateLogin, messages, isTyping, onSend, onNewChat, conversations = [], onNavigateAdmin, onUpdateUser }) {
  const bottomRef = useRef(null);
  const [announcement, setAnnouncement] = useState(null);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  useEffect(() => {
    // Fetch active announcement on mount
    const getAnnouncement = async () => {
      try {
        const data = await fetchAnnouncements();
        if (data.has_announcement) {
          setAnnouncement(data);
        }
      } catch (err) {
        console.error("Failed to load announcements:", err);
      }
    };
    getAnnouncement();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const isGuest = user.type === 'GUEST';
  const isChatEmpty = messages.length === 0;
  
  const displayName = user?.nickname || user?.name || 'User';
  const initial = displayName.charAt(0).toUpperCase();

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
            <div className="user-profile" onClick={() => !isGuest && setIsProfileModalOpen(true)} style={{ cursor: isGuest ? 'default' : 'pointer' }}>
              <div className="avatar">
                {user.avatar_url ? (
                  <img src={user.avatar_url.startsWith('http') ? user.avatar_url : `http://localhost:8000${user.avatar_url}`} alt="Avatar" style={{ width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover' }} />
                ) : (
                  initial
                )}
              </div>
              <div className="user-info">
                <div>{user.nickname || user.name}</div>
                <span>{user.id} {!isGuest && <em style={{ fontSize: '0.8em', marginLeft: '5px', color: 'var(--color-accent)' }}>(Edit)</em>}</span>
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '15px' }}>
              {onNavigateAdmin && (
                <button className="logout-btn" onClick={onNavigateAdmin} style={{ background: 'var(--spus-gold)', color: 'var(--text-dark)', borderColor: 'var(--spus-gold)' }}>
                  Admin Dashboard
                </button>
              )}
              <button className="logout-btn" onClick={onLogout}>Log Out</button>
            </div>
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
          <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
            <ThemeToggle />
            {isGuest && (
              <button 
                onClick={onNavigateLogin} 
                style={{ background: 'none', border: 'none', color: 'var(--color-primary)', fontWeight: 600, cursor: 'pointer', fontSize: '1em' }}
              >
                Login
              </button>
            )}
          </div>
        </header>

        {announcement && (
          <div className="announcement-banner" style={{
            background: 'rgba(212, 175, 55, 0.15)',
            borderBottom: '1px solid var(--color-accent)',
            padding: '12px 20px',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--color-accent)', fontWeight: 600 }}>
              <span>📢</span>
              <span>{announcement.title}</span>
            </div>
            <div style={{ color: 'var(--color-text)', fontSize: '0.9em', lineHeight: 1.4, paddingLeft: '24px' }}>
              {announcement.content}
            </div>
          </div>
        )}

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
                      {msg.isUser ? text : <MarkdownRenderer text={text} />}
                      
                      {!msg.isUser && msg.sources && msg.sources.length > 0 && (
                        <SourcesAccordion sources={msg.sources} />
                      )}

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

      {!isGuest && (
        <EditProfileModal 
          isOpen={isProfileModalOpen} 
          onClose={() => setIsProfileModalOpen(false)} 
          user={user} 
          onUpdate={onUpdateUser}
        />
      )}
    </div>
  );
}
