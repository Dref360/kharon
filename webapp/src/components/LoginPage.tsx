import React from "react";
import { Box, Typography, Paper } from "@mui/material";
import GoogleSignIn from "./GoogleSignIn";
import { useNavigate } from "react-router-dom";

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const handleLoginSuccess = async (idToken: string) => {
    try {
      const response = await fetch("/auth/google", {
        credentials: 'include', // This is important
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ idToken }),
      });

      if (response.ok) {
        navigate("/dashboard");
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
