import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [id, setId] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post('https://jbm-bitcamp.onrender.com/login', {
        id,
        password
      });

      setMessage('Login successful!');
      setError(null);
      console.log(response.data);

      // Store the user data in localStorage
      localStorage.setItem('user', JSON.stringify(response.data));

      // Redirect to dashboard after successful login
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
      setMessage('');
    }
  };

  const isFormValid = id.trim() !== '' && password.trim() !== '';

  return (
    <div className="login-form">
      <div className="whole-page">
        <h2>Login</h2>

        <div className="form-group">
          <input
            type="text"
            placeholder="Email or Username"
            value={id}
            onChange={(e) => setId(e.target.value)}
          />
        </div>

        <div className="form-group">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button 
          className="login-btn" 
          onClick={handleLogin} 
          disabled={!isFormValid}
        >
          Login
        </button>

        {message && <p className="success-message">{message}</p>}
        {error && <p className="error-message">{error}</p>}

        <div className="signup-link">
          <p>Don't have an account?</p>
          <a href="/signup">Sign Up</a>
        </div>
      </div>
    </div>
  );
};

export default Login;
