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
  let { clusterName } = useParams();
  if (!clusterName) {
    return <NotFoundPage />;
  }
  return <ClusterFrame cluster_name={clusterName} />;
};

const ClusterFrame: React.FC<{ cluster_name: string }> = ({ cluster_name }) => {
  /**
   * This component task is to render the user service.
   * It does so by creating an Iframe to ${BACKEND_URL}/clusters/{cluster_name}...
   *
   * Notes:
   *  This is not fool-proof, if a page makes a requests it wont necessarily work.
   *
   * Todo:
   *  To display a loading screen, we probably need to make the request ourselves.
   */
  const [clusterContent, setClusterContent] = useState<ProxyResponse | null>(
    null,
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
  // NOTE the FE path needs to be the same as the BE so /clusters/{name}/other_stuff?param=1
  return (
    <Box sx={{ width: "100%", height: "calc(100vh - 64px)" }}>
      <iframe
        src={`${BACKEND_URL}${window.location.pathname}`}
        style={{ width: "100%", height: "100%", border: "none" }}
        title={`Cluster: ${cluster_name}`}
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
      />
    </Box>
  );
};

export default ProxyRouting;
