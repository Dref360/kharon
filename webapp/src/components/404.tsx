import React from "react";
import { Typography, Paper, Box } from "@mui/material";

const NotFoundPage: React.FC = () => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        404 Not Found
      </Typography>
      <Typography variant="body1">
        We can't find this page. :(
      </Typography>
    </Paper>
  );
};

export default NotFoundPage;
