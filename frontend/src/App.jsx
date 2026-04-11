import { useState, useCallback, useEffect } from 'react';
import './App.css';

import AuthPage from './components/AuthPage';
import RegisterPage from './components/RegisterPage';
import Dashboard from './components/Dashboard';
import AdminDashboard from './components/AdminDashboard';

import { sendMessage, ensureCsrfToken, fetchConversations } from './api/chatApi';

const GUEST_GREETING = "Hello! Welcome to Saint Paul University Surigao! 🤖\n\nI'm PauliBot, your virtual campus assistant. I can help you with admissions, office locations, tuition fees, staff info, and more.\n\nHow may I assist you today?";

export default function App() {
  const [user, setUser] = useState(null); // null = not logged in
  const [currentView, setCurrentView] = useState('login'); // 'login' | 'register' | 'chat'
  
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [conversations, setConversations] = useState([]);

  // Restore session
  useEffect(() => {
    ensureCsrfToken();
    const storedUser = localStorage.getItem('paulibot_user');
    if (storedUser) {
      try {
        const parsed = JSON.parse(storedUser);
        setUser(parsed);
        setCurrentView('chat');
        if (parsed.type === 'GUEST') {
           setMessages([{ text: GUEST_GREETING, isUser: false }]);
        }
      } catch (e) {
        localStorage.removeItem('paulibot_user');
      }
    }
  }, []);

  // Fetch history if student
  useEffect(() => {
    if (user?.type === 'STUDENT') {
      fetchConversations()
        .then(data => setConversations(data))
        .catch(console.error);
    }
  }, [user]);

  const handleLogin = useCallback((userData) => {
    setUser(userData);
    localStorage.setItem('paulibot_user', JSON.stringify(userData));
    
    if (userData.type === 'GUEST') {
      setMessages([{ text: GUEST_GREETING, isUser: false }]);
    } else {
      setMessages([{ text: `Welcome back, ${userData.name}! 🎓 I'm PauliBot... How may I assist you today?`, isUser: false }]);
    }
    setConversationId(null);
    // If superuser, show admin dashboard first; otherwise, go to chat
    if (userData.is_superuser) {
      setCurrentView('admin');
    } else {
      setCurrentView('chat');
    }
  }, []);

  const handleUpdateUser = useCallback((updatedUserData) => {
    setUser(updatedUserData);
    localStorage.setItem('paulibot_user', JSON.stringify(updatedUserData));
  }, []);

  const handleLogout = useCallback(() => {
    setUser(null);
    setMessages([]);
    setConversations([]);
    setConversationId(null);
    localStorage.removeItem('paulibot_user');
    setCurrentView('login');
    fetch('/api/login', { method: 'DELETE', credentials: 'include' }).catch(() => {});
  }, []);

  const handleNewChat = useCallback(() => {
    setMessages([{ text: `Welcome back, ${user.name}! 🎓 How may I assist you today?`, isUser: false }]);
    setConversationId(null);
    fetchConversations().then(data => setConversations(data)).catch(console.error);
  }, [user]);

  const handleSend = useCallback(
    async (text) => {
      setMessages((prev) => [...prev, { text, isUser: true }]);
      setIsTyping(true);

      try {
        const data = await sendMessage(text, conversationId);

        if (data.conversation_id && user?.type === 'STUDENT') {
          setConversationId(data.conversation_id);
          fetchConversations().then(data => setConversations(data)).catch(console.error);
        }

        setTimeout(() => {
          setIsTyping(false);
          setMessages((prev) => [
            ...prev,
            { text: data.response || 'Sorry, I encountered an error.', sources: data.sources || [], action: data.action, isUser: false },
          ]);
        }, 600); // 600ms network delay simulation from your index.html logic
      } catch (err) {
        setIsTyping(false);
        setMessages((prev) => [
          ...prev,
          { text: "Network error. Please try again.", isUser: false },
        ]);
      }
    },
    [conversationId, user]
  );

  // Router Logic
  if (currentView === 'register') {
    return <RegisterPage onNavigateLogin={() => setCurrentView('login')} />;
  }

  if (currentView === 'login' && !user) {
    return <AuthPage onLogin={handleLogin} onNavigateRegister={() => setCurrentView('register')} />;
  }

  // Admin Dashboard (superusers only)
  if (currentView === 'admin' && user?.is_superuser) {
    return (
      <AdminDashboard
        user={user}
        onBackToChat={() => setCurrentView('chat')}
      />
    );
  }

  return (
    <Dashboard
      user={user}
      onLogout={handleLogout}
      onNavigateLogin={() => { handleLogout(); setCurrentView('login'); }}
      messages={messages}
      isTyping={isTyping}
      onSend={handleSend}
      onNewChat={handleNewChat}
      conversations={conversations}
      onNavigateAdmin={user?.is_superuser ? () => setCurrentView('admin') : null}
      onUpdateUser={handleUpdateUser}
    />
  );
}
