import React from 'react';
import { Card, CardContent, Typography, Chip } from '@mui/material';

interface ClusterProps {
  name: string;
  online: boolean;
  url: string;
  description: string;
}

const ClusterCard: React.FC<ClusterProps> = ({ name, online, url, description }) => {
  return (
    <Card sx={{ minWidth: 275, m: 2 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          {name}
        </Typography>
        <Chip 
          label={online ? 'Online' : 'Offline'} 
          color={online ? 'success' : 'error'} 
          size="small" 
          sx={{ mt: 1, mb: 1 }}
        />
        <Typography variant="body2" color="text.secondary">
          URL: {url}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {description}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ClusterCard;