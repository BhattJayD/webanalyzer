import React from "react";
import "./App.css"; // For styling

const ChatInterface = () => {
  return (
    <div className="chat-container">
      <div className="input-box">
        <input type="text" placeholder="What can I help with?" />
        <button className="send-btn">&#9654;</button>
      </div>
    </div>
  );
};

export default ChatInterface;
