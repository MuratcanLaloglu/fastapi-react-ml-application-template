import React, { useEffect, useState } from 'react';
import PredictionForm from './predictionform';
import PaymentForm from './paymentform';
import { getUserDetails } from '../api/auth';

const MainPage = ({ user, onLogout, token, updateUser }) => {
  const [purchasedModels, setPurchasedModels] = useState({});

  useEffect(() => {
    const fetchUserDetails = async () => {
      try {
        const userDetails = await getUserDetails(token);
        setPurchasedModels(userDetails.models || {});
      } catch (error) {
        console.error('Failed to fetch user details', error);
      }
    };

    fetchUserDetails();
  }, [token]);

  return (
    <div>
      <h2>Welcome, {user.username}</h2>
      <p>Email: {user.email}</p>
      <p>Credits: {user.credits}</p>
      <button onClick={onLogout}>Logout</button>
      <h3>Purchased Models</h3>
      <ul>
        {purchasedModels.model1 && <li>Model 1</li>}
        {purchasedModels.model2 && <li>Model 2</li>}
        {purchasedModels.model3 && <li>Model 3</li>}
      </ul>
      <PredictionForm token={token} />
      <PaymentForm token={token} updateUser={updateUser} />
    </div>
  );
};

export default MainPage;