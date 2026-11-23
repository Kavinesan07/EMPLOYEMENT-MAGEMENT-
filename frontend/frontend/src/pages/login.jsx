import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/client';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      // Update '/auth/login' to match your backend login route
      const response = await api.post('/auth/login', { email, password });
      
      // Save token (adjust 'response.data.token' based on your API response)
      localStorage.setItem('token', response.data.token);
      
      // Redirect to the form page after login
      navigate('/dataform');
    } catch (err) {
      setError(err.response?.data?.message || 'Login failed. Check your credentials.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', fontFamily: 'sans-serif' }}>
      <h2>Login</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ padding: '8px' }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ padding: '8px' }}
        />
        <button type="submit" style={{ padding: '10px', cursor: 'pointer' }}>
          Sign In
        </button>
      </form>
    </div>
  );
}
