import axios from 'axios';
import { useState } from 'react';

// Configuration for API endpoint
const API_BASE_URL = 'http://your-backend'; // Replace with your backend URL

const GitHubLogin = ({ onLoginSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Method 1: Using GitHub OAuth2 Redirect (Recommended)
  const handleGitHubOAuth2 = async () => {
    setIsLoading(true);
    setError('');

    try {
      // Get the GitHub OAuth URL from your backend
      const response = await axios.get(`${API_BASE_URL}/accounts/api/github-auth-url/`);
      const { auth_url } = response.data;
      
      // Redirect to GitHub OAuth
      window.location.href = auth_url;
    } catch (err) {
      setError('Failed to initiate GitHub OAuth');
      setIsLoading(false);
    }
  };

  // Method 2: Using GitHub Personal Access Token (For testing)
  const handleGitHubTokenLogin = async () => {
    setIsLoading(true);
    setError('');

    const token = prompt('Enter your GitHub Personal Access Token:');
    if (!token) {
      setIsLoading(false);
      return;
    }

    try {
      // Send access token to your backend
      const backendResponse = await axios.post(`${API_BASE_URL}/accounts/api/github-login/`, {
        access_token: token,
      });

      const { access, refresh, user } = backendResponse.data;
      
      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setIsLoading(false);
      onLoginSuccess();
    } catch (err) {
      setError(err.response?.data?.error || 'GitHub login failed');
      setIsLoading(false);
    }
  };

  // Method 3: Using GitHub OAuth App (Client-side)
  const handleGitHubOAuthApp = async () => {
    setIsLoading(true);
    setError('');

    try {
      // GitHub OAuth App configuration
      const clientId = 'YOUR_GITHUB_CLIENT_ID'; // Replace with your GitHub OAuth App Client ID
      const redirectUri = `${window.location.origin}/auth/github/callback`;
      
      // Build GitHub OAuth URL
      const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=user:email&response_type=code`;
      
      // Redirect to GitHub
      window.location.href = githubAuthUrl;
    } catch (err) {
      setError('Failed to initiate GitHub OAuth');
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h3>Login with GitHub</h3>
      {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
      
      {/* Method 1: OAuth2 Redirect (Recommended) */}
      <div style={{ marginBottom: '15px' }}>
        <button
          onClick={handleGitHubOAuth2}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#24292e',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: 'bold',
          }}
        >
          {isLoading ? 'Redirecting...' : '🐙 Login with GitHub (OAuth2)'}
        </button>
      </div>

      {/* Method 2: Personal Access Token (For testing) */}
      <div style={{ marginBottom: '15px' }}>
        <button
          onClick={handleGitHubTokenLogin}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#28a745',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: 'bold',
          }}
        >
          {isLoading ? 'Authenticating...' : '🔑 Login with GitHub Token'}
        </button>
      </div>

      {/* Method 3: OAuth App (Client-side) */}
      <div>
        <button
          onClick={handleGitHubOAuthApp}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#6f42c1',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            borderRadius: '6px',
            fontSize: '14px',
            fontWeight: 'bold',
          }}
        >
          {isLoading ? 'Redirecting...' : '⚡ Login with GitHub (OAuth App)'}
        </button>
      </div>

      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        <p><strong>Note:</strong> Replace 'YOUR_GITHUB_CLIENT_ID' with your actual GitHub OAuth App Client ID</p>
        <p><strong>API_BASE_URL:</strong> Update with your backend URL</p>
        <p><strong>Token Method:</strong> For testing only - use GitHub Personal Access Token</p>
      </div>
    </div>
  );
};

export default GitHubLogin;
