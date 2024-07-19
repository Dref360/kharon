import React, { useEffect, useState } from "react";
import { Grid, Typography } from "@mui/material";
import ClusterCard from "./ClusterCard";
import { useAuth } from "../helpers/AuthContext";

interface Cluster {
  name: string;
  online: boolean;
  url: string;
  description: string;
  users: string[];
}

interface ClustersResponse {
  clusters: Cluster[];
}

const fetchClusters = async (authToken: string) => {
  return await fetch("/clusters/list", {
    headers: {
      Authorization: `Bearer ${authToken}`,
    },
  })
    .then((res) => res.json())
    .then((res: ClustersResponse) => {
      return res.clusters;
    });
};

const Dashboard: React.FC = () => {
  const { authToken } = useAuth();
  if (!authToken) {
    return (window.location.href = "/login");
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Clusters authToken={authToken} />
    </div>
  );
};

interface DashboardProps {
  authToken: string;
}

const Clusters: React.FC<DashboardProps> = ({ authToken }: DashboardProps) => {
  const [clusters, setClusters] = useState<Cluster[]>([]);

  useEffect(() => {
    const fn = async () => {
      setClusters(await fetchClusters(authToken));
    };
    fn();
  }, [authToken]);

  return (
    <div>
      <Typography variant="h4" gutterBottom sx={{ p: 2 }}>
        Clusters Dashboard
      </Typography>
      <Grid container spacing={2}>
        {clusters.map((cluster, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <ClusterCard {...cluster} />
          </Grid>
        ))}
      </Grid>
    </div>
  );
};

export default Dashboard;
