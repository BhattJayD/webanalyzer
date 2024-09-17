import React from "react";
import "../styles/Vulners.css";
import BarChart from "./BarChart";

export default function Vulners({ res }) {
  console.log(res);

  return (
    <>
      <h2 className="section-title">Services With CVE</h2>

      <BarChart data={res?.search} />
      <div className="json-container">
        {res?.search?.map((item, index) => (
          <div key={index} className="json-card">
            <h3 className="json-header">ID: {item._id}</h3>
            <div className="json-body">
              <p>
                <strong>Index: </strong>
                {item._index}
              </p>
              <p>
                <strong>Score: </strong>
                {item._score}
              </p>
              <p>
                <strong>Family: </strong>
                {item._source.bulletinFamily}
              </p>
              <p>
                <strong>Description: </strong>
                {item._source.description}
              </p>
              <p>
                <strong>More Info: </strong>
                <a href={item._source.href} target="_blank" rel="noreferrer">
                  {item._source.href}
                </a>
              </p>
              <p>
                <strong>Sort Values: </strong>
                {item.sort.join(", ")}
              </p>
            </div>
          </div>
        ))}
      </div>
    </>
  );
}
