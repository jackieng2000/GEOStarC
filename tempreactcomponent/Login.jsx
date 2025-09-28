import axios from 'axios';
import { useState } from 'react';
import GoogleLogin from './GoogleLogin';
import GitHubLogin from './GitHubLogin';

// Configuration for API endpoint
const API_BASE_URL = 'http://your-backend/api'; // Replace with your backend URL

const Login = ({ onLoginSuccess }) => {
  const [hostIP, setHostIP] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await axios.post(`${API_BASE_URL}/token/`, {
        username,
        password,
      });

      const { access, refresh } = response.data;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      setIsLoading(false);
      setHostIP('');
      setUsername('');
      setPassword('');
      onLoginSuccess();
    } catch (err) {
      setIsLoading(false);
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h2>Login to GPS Tracker</h2>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {/* Social Login Section */}
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <GoogleLogin onLoginSuccess={onLoginSuccess} />
        <div style={{ marginTop: '20px', paddingTop: '20px', borderTop: '1px solid #eee' }}>
          <GitHubLogin onLoginSuccess={onLoginSuccess} />
        </div>
      </div>
      
      {/* Divider */}
      <div style={{ textAlign: 'center', margin: '20px 0', position: 'relative' }}>
        <hr style={{ border: 'none', borderTop: '1px solid #ddd' }} />
        <span style={{ background: 'white', padding: '0 15px', color: '#666' }}>OR</span>
      </div>
      
      {/* Traditional Login Form */}
      <form onSubmit={handleLogin}>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="hostIP">Host IP</label>
          <input
            type="text"
            id="hostIP"
            value={hostIP}
            onChange={(e) => setHostIP(e.target.value)}
            placeholder="Enter host IP"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter username"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter password"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            required
          />
        </div>
        <button
          type="submit"
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
          }}
        >
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default Login;