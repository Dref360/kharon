import { Box, Paper, Typography } from "@mui/material";
import React from "react";
import GoogleSignIn from "./GoogleSignIn";
import { make_api_call } from "../api/api";

const LoginPage: React.FC = () => {
  const handleLoginSuccess = async (idToken: string) => {
    await make_api_call({
      path: "/auth/google",
      method: "POST",
      options: {
        body: JSON.stringify({ idToken }),
        headers: {
          "Content-Type": "application/json",
        },
      },
      onSuccess: (res) => {
        if (res.ok) {
          window.location.href = "/";
        } else {
          console.error("Authentication failed");
        }
      },
      onError: (err) => {
        console.error("Error during authentication:", err);
      },
    });
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
