import { RemoveCircle } from "@mui/icons-material";
import {
  Box,
  Button,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";

interface GenerateApiKeyProps {
  authToken: string;
}

interface ApiKeyResponse {
  api_key: string;
}

const GenerateApiKey: React.FC<GenerateApiKeyProps> = ({ authToken }) => {
  const [apiKey, setApiKey] = useState("");
  const [apiKeyName, setAPIKeyName] = useState("");

  const handleGenerateKey = async () => {
    return await fetch(`/app/api-key?key_name=${apiKeyName}`, {
      credentials: "include",
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
    <Box sx={{ p: 1 }}>
      <Typography variant="h5" gutterBottom>
        Generate API Key
      </Typography>
      <Box sx={{ m: 1, display: "flex", gap: 2 }}>
        <TextField
          placeholder="API Key name"
          onChange={(e) => {
            setAPIKeyName(e.target.value);
          }}
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleGenerateKey}
          disabled={!apiKeyName}
        >
          Generate Key
        </Button>
      </Box>
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

interface APIKeyViewModel {
  key_name: string;
  created_at: string;
}

const ListApiKeys: React.FC<GenerateApiKeyProps> = ({ authToken }) => {
  const [keys, setKeys] = useState<APIKeyViewModel[]>([]);
  useEffect(() => {
    const fn = async () => {
      return await fetch(`/app/api-key`, {
        credentials: "include",
        method: "GET",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      })
        .then((res) => res.json())
        .then((res: APIKeyViewModel[]) => {
          setKeys(res);
        });
    };
    fn();
  }, [authToken]);

  const revokeKey = async (key_name: string) => {
    try {
      await fetch(`/app/api-key?key_name=${key_name}`, {
        credentials: "include",
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      });
      setKeys(keys.filter((k) => k.key_name !== key_name));
    } catch (error) {
      console.error("Error adding new user:", error);
    }
  };

  return (
    <Box sx={{ p: 1 }}>
      <Typography variant="h5">API Keys</Typography>
      <TableContainer component={Paper} sx={{ m: 1, maxWidth: 650 }}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell align="left">Created At</TableCell>
              <TableCell align="left">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {keys.map((row) => (
              <TableRow
                key={row.key_name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.key_name}
                </TableCell>
                <TableCell component="th" scope="row">
                  {row.created_at}
                </TableCell>
                <TableCell component="th" scope="row">
                  <IconButton onClick={() => revokeKey(row.key_name)}>
                    <RemoveCircle />
                  </IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

const SettingPage = () => {
  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <GenerateApiKey authToken={"authToken"} />
      <ListApiKeys authToken={"authToken"} />
    </div>
  );
};

export default SettingPage;
