/**
 * ChatContainer Component
 * ========================
 * Scrollable container for the full message history.
 * Manages auto-scrolling on new messages.
 */

import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

export default function ChatContainer({ messages, isTyping, onSuggestionClick }) {
  const bottomRef = useRef(null);

  // Auto-scroll to bottom when messages change or typing starts
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  return (
    <main
      id="chat-window"
      className="flex-1 overflow-y-auto px-4 py-5 flex flex-col gap-4 scroll-smooth"
    >
      {messages.map((msg, i) => (
        <MessageBubble
          key={i}
          text={msg.text}
          isUser={msg.isUser}
          onSuggestionClick={onSuggestionClick}
        />
      ))}

      {isTyping && <TypingIndicator />}

      {/* Invisible scroll anchor */}
      <div ref={bottomRef} />
    </main>
  );
}
