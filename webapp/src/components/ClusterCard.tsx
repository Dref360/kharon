import React, { useState } from "react";
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Button,
  Modal,
  Box,
  Input,
  TextField,
  Grid,
} from "@mui/material";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import { useAuth } from "../helpers/AuthContext";
import OpenInBrowserIcon from "@mui/icons-material/OpenInBrowser";
import { useNavigate } from "react-router-dom";

const modalStyle = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

interface AddUserProps {
  name: string;
  users: string[];
}

const AddUserModal: React.FC<AddUserProps> = ({ name, users }) => {
  const { authToken } = useAuth();
  const [newUser, setNewUser] = useState<string | null>(null);

  // Modal control
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const addNewUser = async () => {
    return await fetch(`/clusters/add_user/${name}?email=${newUser}`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    });
  };

  return (
    <div>
      <Button onClick={handleOpen}>
        <PersonAddIcon />
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={modalStyle}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            User Management
          </Typography>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}>
            <Grid container alignItems="center" sx={{ padding: "5px" }}>
              <Grid item>
                <TextField
                  id="outlined-basic"
                  label="Add a user"
                  variant="outlined"
                  onChange={(e) => setNewUser(e.target.value)}
                />
              </Grid>
              <Grid item>
                <Button onClick={addNewUser} disabled={!newUser}>
                  Submit
                </Button>
              </Grid>
            </Grid>
            {users.length ? (
              users.map((u) => {
                return <Typography>{u}</Typography>;
              })
            ) : (
              <Typography>No user allowed</Typography>
            )}
          </Typography>
        </Box>
      </Modal>
    </div>
  );
};

interface ClusterProps {
  name: string;
  online: boolean;
  url: string;
  description: string;
  users: string[];
}

const ClusterCard: React.FC<ClusterProps> = ({
  name,
  online,
  url,
  description,
  users,
}) => {
  const navigate = useNavigate();
  return (
    <Card sx={{ minWidth: 275, m: 2 }}>
      <CardContent>
        <Grid container justifyContent={"space-around"}>
          <Grid item>
            <Typography variant="h5" component="div">
              {name}
            </Typography>
          </Grid>
          <Grid item>
            <Button
              onClick={() => navigate(`/proxy/${name}`)}
              sx={{ margin: 0 }}
            >
              <OpenInBrowserIcon />
            </Button>
          </Grid>
        </Grid>
        <Chip
          label={online ? "Online" : "Offline"}
          color={online ? "success" : "error"}
          size="small"
          sx={{ mt: 1, mb: 1 }}
        />
        <Grid container spacing={2}>
          <Grid
            item
            xs
            container
            direction="row"
            justifyContent="space-around"
            alignItems="center"
            spacing={2}
          >
            <Grid item>
              <Typography variant="body2" color="text.secondary">
                {description}
              </Typography>
            </Grid>
            <Grid item>
              <AddUserModal name={name} users={users} />
            </Grid>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default ClusterCard;
