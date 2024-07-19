import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import GoogleSignIn from "./GoogleSignIn";
import { useAuth } from "../helpers/AuthContext";
import { useNavigate } from "react-router-dom";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { setAuthToken } = useAuth();
  const handleLoginSuccess = async (idToken: string) => {
    try {
      const response = await fetch("/auth/google", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ idToken }),
      });

      if (response.ok) {
        const data = await response.json();
        // Assuming the server returns a JWT or session token
        setAuthToken(data.access_token);
        navigate("/");
      } else {
        console.error("Authentication failed");
      }
    } catch (error) {
      console.error("Error during authentication:", error);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "background.default",
      }}
    >
      <Paper
        elevation={3}
        sx={{
          padding: 4,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography variant="h4" gutterBottom>
          Login to Kharon
        </Typography>
        <GoogleSignIn onSuccess={handleLoginSuccess} />
      </Paper>
    </Box>
  );
};

export default LoginPage;
