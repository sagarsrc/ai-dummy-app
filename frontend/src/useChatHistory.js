import { useEffect, useState } from 'react';

export function useChatHistory() {
  const [messages, setMessages] = useState([]);

  // Load from localStorage on mount
  useEffect(() => {
    const saved = localStorage.getItem('chat-history');
    if (saved) {
      setMessages(JSON.parse(saved));
    }
  }, []);

  // Save to localStorage whenever messages change
  useEffect(() => {
    localStorage.setItem('chat-history', JSON.stringify(messages));
  }, [messages]);

  return [messages, setMessages];
}
