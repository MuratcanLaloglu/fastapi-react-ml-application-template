import React from 'react';
import PredictionForm from './predictionform';
import PaymentForm from './paymentform';

const MainPage = ({ user, onLogout, token, updateUser }) => {
  const purchasedModels = user.models || {};

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
