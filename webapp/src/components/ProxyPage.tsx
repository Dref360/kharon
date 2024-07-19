import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Box, CircularProgress, Typography } from "@mui/material";
import { useAuth } from "../helpers/AuthContext";

const ClusterFrame: React.FC = () => {
  const { cluster_name } = useParams<{ cluster_name: string }>();
  const { authToken } = useAuth();
  const [clusterContent, setClusterContent] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClusterContent = async () => {
      if (!authToken) return;

      try {
        const response = await fetch(`/clusters/${cluster_name}/`, {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        });

        if (response.ok) {
          const content = await response.text();
          setClusterContent(content);
        } else {
          setError("Failed to fetch cluster content");
        }
      } catch (error) {
        setError("Error fetching cluster content");
        console.error("Error fetching cluster content:", error);
      }
    };

    fetchClusterContent();
  }, [cluster_name, authToken]);

  if (error) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
        }}
      >
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!clusterContent) {
    return (
      <Box
        sx={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ width: "100%", height: "calc(100vh - 64px)" }}>
      <iframe
        srcDoc={clusterContent}
        style={{ width: "100%", height: "100%", border: "none" }}
        title={`Cluster: ${cluster_name}`}
        sandbox="allow-scripts allow-same-origin"
      />
    </Box>
  );
};

export default ClusterFrame;
