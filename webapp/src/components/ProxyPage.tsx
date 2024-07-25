import React, { useState, useEffect, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Box, CircularProgress, Typography } from "@mui/material";
import Home from "./Home";
import NotFoundPage from "./404";

interface ProxyResponse {
  _content: string;
}

const ProxyRouting: React.FC = () => {
  const domain = window.location.hostname;
  const isProxyFrame = domain.split(".").length === 3;
  const clusterName = domain.split(".")[0];
  const navigate = useNavigate();
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

  useEffect(() => {
    const fetchClusterContent = async () => {
      try {
        const response = await fetch(
          `/clusters/${cluster_name}${window.location.pathname}`,
          {
            credentials: "include",
          }
        );

        if (response.ok) {
          const content = await response.json();
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
  }, [cluster_name, params]);

  useEffect(() => {
    const handleIframeLoad = () => {
      if (iframeRef.current) {
        const iframeDocument = iframeRef.current.contentDocument;
        if (iframeDocument) {
          iframeDocument.body.addEventListener("click", (e: MouseEvent) => {
            const target = e.target as HTMLElement;
            if (target.tagName === "A") {
              e.preventDefault();
              const href = target.getAttribute("href");
              if (href) {
                // Check if it's a relative URL
                if (!href.startsWith("/") && !href.startsWith("//")) {
                  navigate(`${window.location.pathname}${href}`);
                } else {
                  // For absolute URLs, you might want to open in a new tab or handle diflferently
                  window.open(href, "_blank");
                }
              }
            }
          });
        }
      }
    };

    if (iframeRef.current) {
      iframeRef.current.addEventListener("load", handleIframeLoad);
    }

    return () => {
      if (iframeRef.current) {
        iframeRef.current.removeEventListener("load", handleIframeLoad);
      }
    };
  }, [cluster_name, navigate, clusterContent]);

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
        ref={iframeRef}
        srcDoc={clusterContent._content}
        style={{ width: "100%", height: "100%", border: "none" }}
        title={`Cluster: ${cluster_name}`}
        sandbox="allow-scripts allow-same-origin"
      />
    </Box>
  );
};

export default ProxyRouting;
