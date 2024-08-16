import CloseIcon from "@mui/icons-material/Close";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import {
  Button,
  Container,
  IconButton,
  Paper,
  Snackbar,
  Typography,
} from "@mui/material";
import React, { useState } from "react";

const Command = () => {
  const [open, setOpen] = useState(false);

  const exportCommand = "export KHARON_API_KEY=";
  const downloadCommand = `curl -O https://raw.githubusercontent.com/Dref360/kharon/main/service/docker-compose.yml && docker-compose up -d`;

  const copyToClipboard = (command: string) => {
    navigator.clipboard.writeText(command).then(() => {
      setOpen(true);
    });
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <Container maxWidth="md" sx={{ mt: 4, p: "10px", display: "inline" }}>
      <Typography variant="h4" gutterBottom>
        Get Started
      </Typography>
      <Typography variant="body1" gutterBottom>
        Generate an API Key in the <a href="/settings">Settings</a> page.
      </Typography>
      <Paper
        elevation={3}
        sx={{
          p: 2,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          backgroundColor: "#f5f5f5",
          overflowX: "auto",
        }}
      >
        <Typography
          variant="body2"
          component="code"
          sx={{
            fontFamily: "monospace",
            whiteSpace: "nowrap",
            overflow: "hidden",
          }}
        >
          {exportCommand}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<ContentCopyIcon />}
          onClick={() => copyToClipboard(exportCommand)}
          sx={{ ml: 2, flexShrink: 0 }}
        >
          Copy
        </Button>
      </Paper>
      <Typography variant="h5" gutterBottom sx={{ mt: "10px" }}>
        Start Your Service
      </Typography>
      <Typography variant="body1" paragraph>
        Run the following command in your terminal to download the
        docker-compose file and start the service:
      </Typography>
      <Paper
        elevation={3}
        sx={{
          p: 2,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          backgroundColor: "#f5f5f5",
          overflowX: "auto",
        }}
      >
        <Typography
          variant="body2"
          component="code"
          sx={{
            fontFamily: "monospace",
            whiteSpace: "nowrap",
            overflow: "hidden",
          }}
        >
          {downloadCommand}
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<ContentCopyIcon />}
          onClick={() => copyToClipboard(downloadCommand)}
          sx={{ ml: 2, flexShrink: 0 }}
        >
          Copy
        </Button>
      </Paper>
      <Snackbar
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "center",
        }}
        open={open}
        autoHideDuration={2000}
        onClose={handleClose}
        message="Command copied to clipboard"
        action={
          <IconButton aria-label="close" color="inherit" onClick={handleClose}>
            <CloseIcon fontSize="small" />
          </IconButton>
        }
      />
    </Container>
  );
};

const Home: React.FC = () => {
  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to Kharon
      </Typography>
      <Typography variant="body1">
        This application allows you to manage webservices safely and easily.
      </Typography>
      <Command />
    </Paper>
  );
};

export default Home;
