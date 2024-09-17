import axios from "axios";
export const postData = async (url) => {
  try {
    const response = await axios.post("http://localhost:5000/scan", {
      url: url,
    });

    console.log("Response:", response.data);
    if (response.data) {
      return response.data;
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

export const postData2 = async (url) => {
  try {
    const response = await axios.post("http://localhost:5000/scanv2", {
      url: url,
    });

    console.log("Response:", response.data);
    if (response.data) {
      return response.data;
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
