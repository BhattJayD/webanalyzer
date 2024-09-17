import React, { useState } from "react";
import "./App.css"; // For styling
import { urlRegex } from "./utils/helper";

const App = () => {
  const [url, setUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents page reload
    if (!url.match(urlRegex)) {
      console.log("not valid url");
      return;
    }
    console.log(url); // Logs the input value
  };

  return (
    <div className="chat-container">
      <form className="input-box" onSubmit={handleSubmit}>
        <input
          type="text"
          onChange={(e) => setUrl(e.target.value)}
          value={url} // Controlled input to manage its value in state
          placeholder="Search for vulnerability on your site"
        />
        <button type="submit" className="send-btn">
          &#9654;
        </button>
      </form>
    </div>
  );
};

export default App;
