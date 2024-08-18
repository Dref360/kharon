import AddBoxIcon from "@mui/icons-material/AddBox";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import RemoveCircleIcon from "@mui/icons-material/RemoveCircle";
import {
  Box,
  Button,
  Card,
  CardActionArea,
  CardActions,
  CardContent,
  CardMedia,
  Chip,
  Grid,
  IconButton,
  Modal,
  TextField,
  Typography,
} from "@mui/material";
import React, { useState } from "react";
import { make_api_call } from "../api/api";

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

interface UserManagementProps {
  name: string;
  users: string[];
}

const UserManagementModal: React.FC<UserManagementProps> = ({
  name,
  users,
}) => {
  const [usersList, setUsersList] = useState(users);
  const [newUser, setNewUser] = useState<string | null>(null);

  // Modal control
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const handleAddUser = async () => {
    if (!newUser) return; // Prevent adding a new user when the input is empty.

    await make_api_call({
      path: `/clusters/add_user/${name}?email=${newUser}`,
      method: "POST",
      onSuccess: (res) => {
        setUsersList(usersList.concat([newUser]));
      },
      onError: (err) => {
        console.error("Error adding new user:", err);
      },
    });
    setNewUser(null);
  };

  const handleRemoveUser = async (userEmail: string) => {
    await make_api_call({
      path: `/clusters/remove_user/${name}?email=${userEmail}`,
      method: "DELETE",
      onSuccess: (res) => {
        setUsersList(usersList.filter((user) => user !== userEmail));
      },
      onError: (err) => {
        console.error("Error adding new user:", err);
      },
    });
    setNewUser(null);
  };

  return (
    <div>
      <Button onClick={handleOpen}>
        Edit Access <PersonAddIcon sx={{ m: "5px" }} />
      </Button>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={modalStyle}>
          <Typography id="modal-modal-title" variant="h5" component="h2">
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
                <IconButton onClick={handleAddUser} disabled={!newUser}>
                  <AddBoxIcon />
                </IconButton>
              </Grid>
            </Grid>
            {/* Users List with Minus Buttons */}
            <Typography variant="h6">Allowed users</Typography>
            <Grid container spacing={2} alignItems="center">
              {usersList.map((user) => (
                <Grid
                  item
                  key={user}
                  sx={{ display: "flex", alignItems: "center" }}
                >
                  <Typography>{user}</Typography>
                  <IconButton
                    onClick={() => handleRemoveUser(user)}
                    color="error"
                  >
                    {/* Minus Button for removing user */}
                    <RemoveCircleIcon />
                  </IconButton>
                </Grid>
              ))}
            </Grid>
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
  return (
    <Card sx={{ minWidth: 275, maxWidth: 275 }}>
      {/*TODO Point to correct link. */}
      <CardActionArea
        onClick={() => {
          window.location.href = `/clusters/${name}/`;
        }}
      >
        <CardMedia
          sx={{ height: 140 }}
          image="/assets/web-development.png"
          title="Webstuff"
        />
        <CardContent sx={{ display: "block" }}>
          <Typography variant="h5" component="div">
            {name}
          </Typography>
          <Chip
            label={online ? "Online" : "Offline"}
            color={online ? "success" : "error"}
            size="small"
            sx={{ mt: 1, mb: 1 }}
          />
          <Typography variant="body2" color="text.secondary">
            {description}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions>
        <UserManagementModal name={name} users={users} />
      </CardActions>
    </Card>
  );
};

export default ClusterCard;
