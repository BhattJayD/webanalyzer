import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

const PieChart = ({ services }) => {
  console.log(services, "sss");

  // Determine the number of services with data and without data
  const servicesWithData = services?.filter(
    (service) => service.vulns.length > 0
  ).length;

  console.log(services.length, "servicesWithoutData");

  const data = {
    labels: ["Services without exploit", "Services with exploit"],
    datasets: [
      {
        data: [servicesWithData, services.length],
        backgroundColor: ["#FF6384", "#36A2EB"], // Red for data, Green for no data
        hoverBackgroundColor: ["#FF6384", "#36A2EB"],
      },
    ],
  };

  const options = {
    plugins: {
      legend: {
        display: true,
        position: "bottom",
      },
    },
  };

  return (
    <div style={{ width: "400px", margin: "auto" }}>
      <h3>Services Data Overview</h3>
      <Pie data={data} options={options} />
    </div>
  );
};

export default PieChart;
