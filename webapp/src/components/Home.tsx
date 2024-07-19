import React from "react";
import { Typography, Paper, Box } from "@mui/material";

const Home: React.FC = () => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to Kharon
      </Typography>
      <Typography variant="body1">
        This application allows you to manage webservices safely and easily.
      </Typography>
    </Paper>
  );
};

export default Home;
