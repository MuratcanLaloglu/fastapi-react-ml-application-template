import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const makePrediction = async (modelName, inputData, token) => {
  const response = await axios.post(`${API_URL}/predict/${modelName}`, inputData, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  return response.data;
};
