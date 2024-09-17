import React, { useState } from "react";
import "./App.css"; // For styling
import { urlRegex } from "./utils/helper";
import { postData, postData2 } from "./api/api";
import PieChart from "./PieChart";

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

      {res != "" && <PieChart services={res.exploits} />}

      {res?.services && (
        <div className="results-container">
          <h2 className="section-title">Services and Versions</h2>
          <div className="card-list">
            {res.services.map((service, index) => {
              const [name, version] = splitString(service);
              return (
                <div key={index} className="service-card">
                  <h3 className="service-name">{name}</h3>
                  <p className="service-version">Version: {version}</p>
                </div>
              );
            })}
          </div>

          <h2 className="section-title">Exploits</h2>
          <div className="card-list">
            {res.exploits.map((i, l) => (
              <div key={l} className="exploit-card">
                <h3 className="exploit-service">{i.service}</h3>
                <ul className="exploit-list">
                  {i.vulns.map((e, key) => (
                    <li key={key} className="exploit-item">
                      {e}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
