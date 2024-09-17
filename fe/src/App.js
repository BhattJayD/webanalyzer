import React from "react";
import "./App.css"; // For styling

const App = () => {
  return (
    <div className="chat-container">
      <div className="input-box">
        <input
          type="text"
          placeholder="Search for vulnerability on your site"
        />
        <button className="send-btn">&#9654;</button>
      </div>
    </div>
  );
};

export default App;
