import React, { useState } from "react";
import { Button, TextField, Box, Typography } from "@mui/material";

interface GenerateApiKeyProps {
  authToken: string;
}

interface ApiKeyResponse {
  api_key: string;
}

const GenerateApiKey: React.FC<GenerateApiKeyProps> = ({ authToken }) => {
  const [apiKey, setApiKey] = useState("");

  const handleGenerateKey = async () => {
    // This is a placeholder. In a real app, you'd call an API to generate the key.
    return await fetch("/app/api-key", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })
      .then((res) => res.json())
      .then((res: ApiKeyResponse) => {
        setApiKey(res.api_key);
      });
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Generate API Key
      </Typography>
      <Button variant="contained" color="primary" onClick={handleGenerateKey}>
        Generate Key
      </Button>
      {apiKey && (
        <TextField
          fullWidth
          margin="normal"
          label="Generated API Key"
          value={apiKey}
          InputProps={{ readOnly: true }}
        />
      )}
    </Box>
  );
};

export default GenerateApiKey;
