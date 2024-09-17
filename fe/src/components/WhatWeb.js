import React from "react";
import "../App.css";
import PieChart from "../PieChart";

export default function WhatWeb({ res }) {
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
    <div>
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
                <h3 className="exploit-service">{i?.service}</h3>
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
}
