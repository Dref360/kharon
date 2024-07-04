import React, { useState } from "react";
import { ThemeProvider } from "@mui/material/styles";
import {
  CssBaseline,
  AppBar,
  Toolbar,
  Typography,
  Tabs,
  Tab,
  Box,
  Button,
} from "@mui/material";
import theme from "./theme";
import Dashboard from "./components/Dashboard";
import LoginPage from "./components/LoginPage";
import GenerateApiKey from "./components/GenerateAPIKey";

const App: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [authToken, setAuthToken] = useState<string | null>(null);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleLogin = (token: string) => {
    setAuthToken(token);
    // You might want to store the token in localStorage here
    // localStorage.setItem('authToken', token);
  };

  const handleLogout = () => {
    setAuthToken(null);
    // Clear the token from localStorage if you stored it there
    // localStorage.removeItem('authToken');
  };

  if (!authToken) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <LoginPage onLogin={handleLogin} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Cluster Management
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
        <Tabs value={tabValue} onChange={handleTabChange} centered>
          <Tab label="Dashboard" />
          <Tab label="Generate API Key" />
        </Tabs>
      </AppBar>
      <Box sx={{ p: 3 }}>
        {tabValue === 0 && <Dashboard authToken={authToken} />}
        {tabValue === 1 && <GenerateApiKey authToken={authToken} />}
      </Box>
    </ThemeProvider>
  );
};

export default App;
