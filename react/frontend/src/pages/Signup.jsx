import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  const handleSignup = async () => {
    try {
      const response = await axios.post('https://jbm-bitcamp.onrender.com/signup', {
        email,
        username,
        password
      });

      setMessage('Signup successful!');
      setError(null);
      console.log(response.data);

      // Redirect to dashboard after successful signup
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Signup failed');
      setMessage('');
    }
  };

  const isFormValid = email.trim() !== '' && username.trim() !== '' && password.trim() !== '';

  return (
    <div className="signup-form">
      <div className="whole-page">
        <h2>Sign Up</h2>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        /><br />

        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        /><br />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        /><br />

        <button onClick={handleSignup} disabled={!isFormValid}>
          Sign Up
        </button>

        {message && <p style={{ color: 'green' }}>{message}</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </div>
  );
};

export default Signup;
