import { Box, CircularProgress, Typography } from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { BACKEND_URL, make_api_call } from "../api/api";
import NotFoundPage from "./404";
import Home from "./Home";

interface ProxyResponse {
  _content: string;
}

const ProxyRouting: React.FC = () => {
  const domain = window.location.hostname;
  const isProxyFrame = domain.split(".").length === 3;
  const clusterName = domain.split(".")[0];
  console.log(domain);

  if (!isProxyFrame) {
    if (window.location.pathname === "/") {
      return <Home />;
    } else {
      return <NotFoundPage />;
    }
  }
  return <ClusterFrame cluster_name={clusterName} />;
};

const ClusterFrame: React.FC<{ cluster_name: string }> = ({ cluster_name }) => {
  const [clusterContent, setClusterContent] = useState<ProxyResponse | null>(
    null
  );
  const [error, setError] = useState<string | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const navigate = useNavigate();
  const params = useParams();

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

  return (
    <Box sx={{ width: "100%", height: "calc(100vh - 64px)" }}>
      <iframe
        src={`${BACKEND_URL}/clusters/${cluster_name}${window.location.pathname}`}
        style={{ width: "100%", height: "100%", border: "none" }}
        title={`Cluster: ${cluster_name}`}
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
      />
    </Box>
  );
};

export default ProxyRouting;
