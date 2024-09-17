import React from "react";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import "../styles/BarChart.css"; // Custom CSS for styling

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const BarChart = ({ data }) => {
  // Prepare labels and score data for the chart
  const labels = data.map((item) => item._id); // You can use a different label if needed
  const scores = data.map((item) => item._score);

  const chartData = {
    labels: labels, // IDs or names as labels
    datasets: [
      {
        label: "Scores",
        data: scores, // Corresponding scores
        backgroundColor: "rgba(75, 192, 192, 0.6)",
        borderColor: "rgba(75, 192, 192, 1)",
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Vulnerability Scores",
      },
    },
  };

  return (
    <div className="bar-chart-container">
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default BarChart;
