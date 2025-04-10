import React from 'react';

const ChatMessage = ({ message }) => {
  const { role, content } = message;
  const isUser = role === 'user';
  
  // Function to render message content based on type
  const renderContent = () => {
    if (typeof content === 'string') {
      return <p>{content}</p>;
    } else if (Array.isArray(content)) {
      return (
        <>
          {content.map((item, index) => {
            if (item.type === 'text') {
              return <p key={index}>{item.text}</p>;
            } else if (item.type === 'tool_call_result') {
              const result = item.tool_call_result;
              
              // Display file content when available
              if (result.content) {
                return (
                  <div key={index} className="tool-result">
                    <p className="font-bold mb-1">File Content:</p>
                    <pre className="whitespace-pre-wrap">{result.content}</pre>
                  </div>
                );
              }
              
              // Display error if any
              if (result.error) {
                return (
                  <div key={index} className="tool-result text-red-500">
                    <p className="font-bold mb-1">Error:</p>
                    <p>{result.error}</p>
                  </div>
                );
              }
              
              // Generic tool result
              return (
                <div key={index} className="tool-result">
                  <p className="font-bold mb-1">Tool Result:</p>
                  <pre className="whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
                </div>
              );
            }
            return null;
          })}
        </>
      );
    }
    return null;
  };

  return (
    <div className={`message-container ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className={`font-bold mb-1 ${isUser ? 'text-blue-900':'text-orange-600'}`}>{isUser ? 'You' : 'Assistant'}</div>
      {renderContent()}
    </div>
  );
};

export default ChatMessage;