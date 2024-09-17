import React, { useState } from "react";
import "./App.css"; // For styling
import { urlRegex } from "./utils/helper";
import { postData, postData2 } from "./api/api";
import WhatWeb from "./components/WhatWeb";
import Vulners from "./components/Vulners";

const App = () => {
  const [url, setUrl] = useState("");
  const [res, setRes] = useState("");
  const [res1, setRes1] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevents page reload
    if (!url.match(urlRegex)) {
      console.log("not valid url");
      return;
    }
    console.log(url); // Logs the input value
    const r1 = await postData(url);
    const r2 = await postData2(url);
    setRes(r1);
    setRes1(r2);
  };

  function splitString(input) {
    // Use a regular expression to separate the string into parts
    const parts = input.match(/(\D+)\s+([\d.]+)/);

    if (parts) {
      // Return the name part and the version as a float-like string
      return [parts[1].trim(), parts[2]];
    } else {
      // Return null or handle the case where the format is not as expected
      return null;
    }
  }

  return (
    <div className="chat-container">
      <form className="input-box" onSubmit={handleSubmit}>
        <input
          type="text"
          onChange={(e) => setUrl(e.target.value)}
          value={url} // Controlled input to manage its value in state
          placeholder="Search for vulnerability on your site"
          className="input-field"
        />
        <button type="submit" className="send-btn">
          &#9654;
        </button>
      </form>

      {res != "" && <WhatWeb res={res} />}
      {res1 != "" && <Vulners res={res1?.vulnerabilities?.data} />}
    </div>
  );
};

export default App;
