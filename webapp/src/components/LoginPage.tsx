import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import GoogleSignIn from './GoogleSignIn';

interface LoginPageProps {
  onLogin: (token: string) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLogin }) => {
  const handleLoginSuccess = async (idToken: string) => {
    try {
      const response = await fetch('/auth/google', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idToken }),
      });

      if (response.ok) {
        const data = await response.json();
        // Assuming the server returns a JWT or session token
        onLogin(data.access_token);
      } else {
        console.error('Authentication failed');
      }
    } catch (error) {
      console.error('Error during authentication:', error);
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        backgroundColor: 'background.default',
      }}
    >
      <Paper elevation={3} sx={{ padding: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h4" gutterBottom>
          Login to Shared Science
        </Typography>
        <GoogleSignIn onSuccess={handleLoginSuccess} />
      </Paper>
    </Box>
  );
};

export default LoginPage;