import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import MessageInput from './MessageInput';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (text) => {
    // Add user message to chat
    console.log("message in HandleSendMessage in chatinterface.jsx: ",text)
    const userMessage = { role: 'user', content: text };
    const updatedMessages = [...messages, userMessage]; 
    console.log("updatedMessages in HandleSendMessage in chatinterface.jsx: ",updatedMessages)
    setMessages(updatedMessages);
    
    // Show loading state
    setIsLoading(true);
    
    try {
      // Send message to backend
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          messages: updatedMessages
        }),
      });
      console.log("response at chatInterface: ",response)
      
      if (!response.ok) {
        throw new Error('Failed to get response');
      }
      
      const data = await response.json();
      console.log("data in handleSendMessage: ",data)
      
      // Add assistant response to chat
      setMessages((prevMessages) => [...prevMessages, data.message]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      setMessages((prevMessages) => [
        ...prevMessages,
        { 
          role: 'assistant', 
          content: 'Sorry, I encountered an error processing your request.' 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container rounded-md border-2 bg-gradient-to-r from-teal-500 to-violet-700">
      <div className="bg-white rounded-lg shadow-md p-4 mb-4">
        <h1 className="text-3xl font-bold mb-4 text-center text-blue-500">Chat with <p className='inline bg-gradient-to-r from-orange-500 to-violet-700 bg-clip-text text-transparent'>Gemini</p></h1>
        
        <div className="h-96 overflow-y-auto mb-4 p-2">
          {messages.length === 0 ? (
            <p className="text-gray-400 text-center text-3xl">Start a conversation by sending a message!</p>
          ) : (
            messages.map((message, index) => (
              <ChatMessage key={index} message={message} />
            ))
          )}
          
          {isLoading && (
            <div className="message-container assistant-message">
              <div className="font-bold mb-1 text-orange-600">Assistant</div>
              <p>Thinking...</p>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        <MessageInput onSendMessage={handleSendMessage} />
      </div>
      
      <div className="text-md text-blue-100 text-center">
        <p>Try asking: "Read file test.txt"</p>
      </div>
    </div>
  );
};

export default ChatInterface;