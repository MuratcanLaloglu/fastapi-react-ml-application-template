import React, { useState, useEffect } from 'react';
import RegisterForm from './components/registerform';
import LoginForm from './components/loginform';
import MainPage from './components/mainpage';
import { getCurrentUser } from './api/user';

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(null);

  const fetchUser = async () => {
    if (token) {
      try {
        const data = await getCurrentUser(token);
        setUser(data);
      } catch (error) {
        console.error('Failed to fetch user');
      }
    }
  };

  useEffect(() => {
    fetchUser();
  }, [token]);

  useEffect(() => {
    localStorage.setItem('token', token);
  }, [token]);

  const handleLogout = () => {
    setToken('');
    setUser(null);
  };

  return (
    <div>
      {user ? (
        <MainPage user={user} onLogout={handleLogout} token={token} updateUser={fetchUser} />
      ) : (
        <div>
          <RegisterForm />
          <LoginForm setToken={setToken} />
        </div>
      )}
    </div>
  );
};

export default App;
