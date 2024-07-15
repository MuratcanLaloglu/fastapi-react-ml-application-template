import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const makePayment = async (option, token) => {
  const response = await axios.post(`${API_URL}/api/payment/${option}`, {}, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.data;
};
