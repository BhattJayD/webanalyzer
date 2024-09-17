import axios from "axios";
// require("dotenv").config();

axios.defaults.baseURL = "http://localhost:5000/";
export const postData = async (url) => {
  try {
    const response = await axios.post("scan", {
      url: url,
    });

    console.log("Response:", response.data);
    if (response.data) {
      return response?.data;
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

export const postData2 = async (url) => {
  try {
    const response = await axios.post("scanv2", {
      url: url,
    });

    console.log("Response:", response.data);
    if (response.data) {
      return response?.data;
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
