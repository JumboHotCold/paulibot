/**
 * TypingIndicator Component
 * ==========================
 * Animated bouncing dots shown while PauliBot is generating a response.
 */

export default function TypingIndicator() {
  return (
    <div className="flex justify-start animate-message-in">
      <div className="bg-msg-bot border border-glass-border rounded-2xl rounded-bl-sm px-5 py-3.5 flex items-center gap-1.5 shadow-md">
        <span className="typing-dot w-2 h-2 rounded-full bg-text-secondary" />
        <span className="typing-dot w-2 h-2 rounded-full bg-text-secondary" />
        <span className="typing-dot w-2 h-2 rounded-full bg-text-secondary" />
      </div>
    </div>
  );
}
