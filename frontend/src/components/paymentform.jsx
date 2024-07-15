import React, { useState } from 'react';
import { makePayment } from '../api/payment';

const PaymentForm = ({ token, updateUser }) => {
  const [option, setOption] = useState('model1');
  const [message, setMessage] = useState('');

  const handlePayment = async (e) => {
    e.preventDefault();
    try {
      const result = await makePayment(option, token);
      setMessage(result.message);
      updateUser(); // Fetch updated user info
    } catch (error) {
      setMessage('Payment failed');
    }
  };

  return (
    <div>
      <form onSubmit={handlePayment}>
        <h2>Make a Payment</h2>
        <select value={option} onChange={(e) => setOption(e.target.value)}>
          <option value="model1">Model 1 - $30</option>
          <option value="model2">Model 2 - $60</option>
          <option value="model3">Model 3 - $90</option>
          <option value="all">All Models - $100</option>
        </select>
        <button type="submit">Pay</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default PaymentForm;
