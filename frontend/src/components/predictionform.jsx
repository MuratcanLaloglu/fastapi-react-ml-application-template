import React, { useState } from 'react';
import { makePrediction } from '../api/prediction';

const PredictionForm = ({ token }) => {
  const [inputData, setInputData] = useState({
    married: 0,
    income: '',
    education: 1,
    loan_amount: '',
    credit_history: 1,
    model: 'model1'
  });

  const [prediction, setPrediction] = useState(null);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setInputData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await makePrediction(inputData.model, inputData, token);
      setPrediction(result.prediction);
      setMessage(`Prediction: ${result.prediction}, Credits Left: ${result.credits_left}`);
    } catch (error) {
      setMessage('Prediction failed');
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h2>Make a Prediction</h2>
        <div>
          <label>Married:</label>
          <select name="married" value={inputData.married} onChange={handleChange}>
            <option value={0}>Not Married</option>
            <option value={1}>Married</option>
          </select>
        </div>
        <div>
          <label>Income:</label>
          <input
            type="number"
            name="income"
            value={inputData.income}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Education:</label>
          <select name="education" value={inputData.education} onChange={handleChange}>
            <option value={1}>Graduated</option>
            <option value={2}>Not Graduated</option>
          </select>
        </div>
        <div>
          <label>Loan Amount:</label>
          <input
            type="number"
            name="loan_amount"
            value={inputData.loan_amount}
            onChange={handleChange}
            required
          />
        </div>
        <div>
          <label>Credit History:</label>
          <select name="credit_history" value={inputData.credit_history} onChange={handleChange}>
            <option value={1}>Yes</option>
            <option value={2}>No</option>
          </select>
        </div>
        <div>
          <label>Model:</label>
          <select name="model" value={inputData.model} onChange={handleChange}>
            <option value="model1">Model 1</option>
            <option value="model2">Model 2</option>
            <option value="model3">Model 3</option>
          </select>
        </div>
        <button type="submit">Predict</button>
      </form>
      {message && <p>{message}</p>}
      {prediction !== null && <p>Prediction: {prediction}</p>}
    </div>
  );
};

export default PredictionForm;
