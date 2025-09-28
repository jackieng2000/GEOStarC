import axios from 'axios';
import { useState } from 'react';

// Configuration for API endpoint
const API_BASE_URL = 'http://your-backend'; // Replace with your backend URL

const GoogleLogin = ({ onLoginSuccess }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Method 1: Using Google Identity Services (Recommended)
  const handleGoogleLogin = async () => {
    setIsLoading(true);
    setError('');

    try {
      // Load Google Identity Services
      if (!window.google) {
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
        
        await new Promise((resolve) => {
          script.onload = resolve;
        });
      }

      // Initialize Google Identity Services
      window.google.accounts.id.initialize({
        client_id: 'YOUR_GOOGLE_CLIENT_ID', // Replace with your Google Client ID
        callback: handleCredentialResponse,
        auto_select: false,
        cancel_on_tap_outside: true,
      });

      // Render the Google Sign-In button
      window.google.accounts.id.renderButton(
        document.getElementById('google-signin-button'),
        {
          theme: 'outline',
          size: 'large',
          width: '100%',
          text: 'signin_with',
          shape: 'rectangular',
        }
      );

    } catch (err) {
      setError('Failed to initialize Google Sign-In');
      setIsLoading(false);
    }
  };

  const handleCredentialResponse = async (response) => {
    try {
      // Send the credential to your backend
      const backendResponse = await axios.post(`${API_BASE_URL}/accounts/api/google-login/`, {
        credential: response.credential,
      });

      const { access, refresh, user } = backendResponse.data;
      
      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setIsLoading(false);
      onLoginSuccess();
    } catch (err) {
      setError(err.response?.data?.error || 'Google login failed');
      setIsLoading(false);
    }
  };

  // Method 2: Using Google OAuth2 (Alternative approach)
  const handleGoogleOAuth2 = async () => {
    setIsLoading(true);
    setError('');

    try {
      // Get the Google OAuth URL from your backend
      const response = await axios.get(`${API_BASE_URL}/accounts/api/google-auth-url/`);
      const { auth_url } = response.data;
      
      // Redirect to Google OAuth
      window.location.href = auth_url;
    } catch (err) {
      setError('Failed to initiate Google OAuth');
      setIsLoading(false);
    }
  };

  // Method 3: Using Google JavaScript API (Legacy but still works)
  const handleGoogleJSAPI = async () => {
    setIsLoading(true);
    setError('');

    try {
      // Load Google API
      if (!window.gapi) {
        const script = document.createElement('script');
        script.src = 'https://apis.google.com/js/api.js';
        script.async = true;
        script.defer = true;
        document.head.appendChild(script);
        
        await new Promise((resolve) => {
          script.onload = resolve;
        });
      }

      // Initialize Google API
      await new Promise((resolve, reject) => {
        window.gapi.load('auth2', () => {
          window.gapi.auth2.init({
            client_id: 'YOUR_GOOGLE_CLIENT_ID', // Replace with your Google Client ID
          }).then(resolve).catch(reject);
        });
      });

      // Sign in with Google
      const authInstance = window.gapi.auth2.getAuthInstance();
      const googleUser = await authInstance.signIn();
      const accessToken = googleUser.getAuthResponse().access_token;

      // Send access token to your backend
      const backendResponse = await axios.post(`${API_BASE_URL}/accounts/api/google-login/`, {
        access_token: accessToken,
      });

      const { access, refresh, user } = backendResponse.data;
      
      // Store tokens
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      localStorage.setItem('user', JSON.stringify(user));
      
      setIsLoading(false);
      onLoginSuccess();
    } catch (err) {
      setError(err.response?.data?.error || 'Google login failed');
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
      <h3>Login with Google</h3>
      {error && <p style={{ color: 'red', marginBottom: '15px' }}>{error}</p>}
      
      {/* Method 1: Google Identity Services Button */}
      <div style={{ marginBottom: '15px' }}>
        <div id="google-signin-button"></div>
        <button
          onClick={handleGoogleLogin}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#4285f4',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
            marginTop: '10px',
          }}
        >
          {isLoading ? 'Loading...' : 'Initialize Google Sign-In'}
        </button>
      </div>

      {/* Method 2: OAuth2 Redirect */}
      <div style={{ marginBottom: '15px' }}>
        <button
          onClick={handleGoogleOAuth2}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#34a853',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
          }}
        >
          {isLoading ? 'Redirecting...' : 'Login with Google (OAuth2)'}
        </button>
      </div>

      {/* Method 3: JavaScript API */}
      <div>
        <button
          onClick={handleGoogleJSAPI}
          disabled={isLoading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: isLoading ? '#ccc' : '#ea4335',
            color: 'white',
            border: 'none',
            cursor: isLoading ? 'not-allowed' : 'pointer',
          }}
        >
          {isLoading ? 'Signing in...' : 'Login with Google (JS API)'}
        </button>
      </div>

      <div style={{ marginTop: '20px', fontSize: '12px', color: '#666' }}>
        <p><strong>Note:</strong> Replace 'YOUR_GOOGLE_CLIENT_ID' with your actual Google Client ID</p>
        <p><strong>API_BASE_URL:</strong> Update with your backend URL</p>
      </div>
    </div>
  );
};

export default GoogleLogin;

