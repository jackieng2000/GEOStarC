# Social Login Setup Guide (Google & GitHub)

This guide will help you set up Google and GitHub social login for your Django GPS tracking system.

## Prerequisites

1. A Google Cloud Platform account
2. A GitHub account
3. Your Django project running
4. Access to your server/development environment

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 3: Set Up OAuth Credentials

### 3.1 Set Up Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google Identity API)
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Choose "Web application"
6. Add authorized redirect URIs:
   - For development: `http://localhost:8000/accounts/google/login/callback/`
   - For production: `https://yourdomain.com/accounts/google/login/callback/`
7. Copy the Client ID and Client Secret

### 3.2 Set Up GitHub OAuth

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the application details:
   - **Application name**: Your GPS Tracker App
   - **Homepage URL**: Your app URL
   - **Authorization callback URL**: 
     - For development: `http://localhost:8000/accounts/github/login/callback/`
     - For production: `https://yourdomain.com/accounts/github/login/callback/`
4. Click "Register application"
5. Copy the Client ID and Client Secret

### 3.3 Configure Environment Variables

Create a `.env` file in your project root (or set environment variables):

```bash
# Google OAuth Configuration
GOOGLE_OAUTH2_CLIENT_ID=your-google-client-id-here
GOOGLE_OAUTH2_SECRET=your-google-client-secret-here

# GitHub OAuth Configuration
GITHUB_OAUTH2_CLIENT_ID=your-github-client-id-here
GITHUB_OAUTH2_SECRET=your-github-client-secret-here
```

## Step 4: Update Django Settings

The settings have been updated in `rbackend/settings.py`. Make sure to set your environment variables:

```python
# Add these to your settings.py or use environment variables
GOOGLE_OAUTH2_CLIENT_ID = os.getenv('GOOGLE_OAUTH2_CLIENT_ID')
GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_OAUTH2_SECRET')
GITHUB_OAUTH2_CLIENT_ID = os.getenv('GITHUB_OAUTH2_CLIENT_ID')
GITHUB_OAUTH2_SECRET = os.getenv('GITHUB_OAUTH2_SECRET')
```

## Step 5: Create Superuser and Configure Admin

```bash
python manage.py createsuperuser
python manage.py runserver
```

1. Go to Django Admin: `http://localhost:8000/admin/`
2. Navigate to "Sites" and update the domain name
3. Go to "Social Applications" and add applications:

   **Google Application:**
   - Provider: Google
   - Name: Google
   - Client ID: Your Google Client ID
   - Secret Key: Your Google Client Secret
   - Sites: Select your site

   **GitHub Application:**
   - Provider: GitHub
   - Name: GitHub
   - Client ID: Your GitHub Client ID
   - Secret Key: Your GitHub Client Secret
   - Sites: Select your site

## Step 6: Test the Integration

### Backend Testing

1. Start your Django server:
   ```bash
   python manage.py runserver
   ```

2. Test the OAuth URL endpoints:
   ```bash
   # Test Google auth URL
   curl http://localhost:8000/accounts/api/google-auth-url/
   
   # Test GitHub auth URL
   curl http://localhost:8000/accounts/api/github-auth-url/
   ```

3. Test the login endpoints:
   ```bash
   # Test Google login (with mock token)
   curl -X POST http://localhost:8000/accounts/api/google-login/ \
     -H "Content-Type: application/json" \
     -d '{"access_token": "mock_token"}'
   
   # Test GitHub login (with mock token)
   curl -X POST http://localhost:8000/accounts/api/github-login/ \
     -H "Content-Type: application/json" \
     -d '{"access_token": "mock_token"}'
   ```

### Frontend Testing

1. Update the `API_BASE_URL` in your React components
2. Replace `YOUR_GOOGLE_CLIENT_ID` and `YOUR_GITHUB_CLIENT_ID` with your actual Client IDs
3. Test both Google and GitHub login flows

## Step 7: Production Deployment

### Environment Variables

Set these environment variables on your production server:

```bash
export GOOGLE_OAUTH2_CLIENT_ID="your-production-google-client-id"
export GOOGLE_OAUTH2_SECRET="your-production-google-client-secret"
export GITHUB_OAUTH2_CLIENT_ID="your-production-github-client-id"
export GITHUB_OAUTH2_SECRET="your-production-github-client-secret"
```

### Update OAuth Settings

1. **Google OAuth:**
   - Add your production domain to authorized redirect URIs
   - Update the Django admin with production credentials

2. **GitHub OAuth:**
   - Update the Authorization callback URL in GitHub OAuth App settings
   - Update the Django admin with production credentials

3. Ensure HTTPS is enabled for production

## API Endpoints

The following endpoints are now available:

**Google OAuth:**
- `GET /accounts/api/google-auth-url/` - Get Google OAuth URL
- `POST /accounts/api/google-login/` - Handle Google login with access token
- `GET /accounts/google/login/` - Django Allauth Google login
- `GET /accounts/google/login/callback/` - Google OAuth callback

**GitHub OAuth:**
- `GET /accounts/api/github-auth-url/` - Get GitHub OAuth URL
- `POST /accounts/api/github-login/` - Handle GitHub login with access token
- `GET /accounts/github/login/` - Django Allauth GitHub login
- `GET /accounts/github/login/callback/` - GitHub OAuth callback

## Frontend Integration

**Google Login (`GoogleLogin.jsx`):**
1. **Google Identity Services** (Recommended) - Modern, secure
2. **OAuth2 Redirect** - Server-side flow
3. **JavaScript API** - Legacy but reliable

**GitHub Login (`GitHubLogin.jsx`):**
1. **OAuth2 Redirect** (Recommended) - Server-side flow
2. **Personal Access Token** - For testing only
3. **OAuth App** - Client-side flow

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI"**
   - Check that your redirect URI in Google Console matches exactly
   - Ensure protocol (http/https) is correct

2. **"Client ID not found"**
   - Verify your Google Client ID is correct
   - Check environment variables are loaded

3. **"Access denied"**
   - Ensure Google+ API is enabled
   - Check OAuth consent screen is configured

4. **CORS errors**
   - Update CORS settings in Django
   - Ensure frontend domain is in allowed origins

### Debug Mode

Enable debug logging in Django settings:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'allauth': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## Security Considerations

1. **Never commit credentials** to version control
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** in production
4. **Set proper CORS policies**
5. **Validate tokens** on the backend
6. **Use secure session settings** in production

## Next Steps

1. Test the complete authentication flow
2. Integrate with your existing user management
3. Add error handling and user feedback
4. Consider adding other social providers (Facebook, GitHub, etc.)
5. Implement proper logging and monitoring

## Support

If you encounter issues:

1. Check Django logs for errors
2. Verify Google OAuth configuration
3. Test with different browsers/devices
4. Check network requests in browser dev tools
5. Review Google Cloud Console logs

