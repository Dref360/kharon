import { useGoogleLogin } from "@react-oauth/google";
import React, { createContext, useContext, useState } from "react";

const BACKEND_URL = "http://0.0.0.0:8000";

const UserInfoContext = createContext({
  userInfo: null,
  setUserInfo: () => {},
});
export const UserInfoProvider = ({ children }) => {
  const [userInfo, setUserInfo] = useState(null);
  return (
    <UserInfoContext.Provider value={{ userInfo, setUserInfo }}>
      {children}
    </UserInfoContext.Provider>
  );
};

export const useUserInfoContext = () => useContext(UserInfoContext);

export const GoogleSignIn = () => {
  const { setUserInfo } = useUserInfoContext();
  const handleSuccess = (credentialResponse) => {
    // If you are using the authorization code flow, you will receive a code to be exchanged for an access token
    const authorizationCode = credentialResponse.code;
    console.log(authorizationCode);
    // Send the authorization code to your backend server
    fetch(`${BACKEND_URL}/auth/google`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: authorizationCode }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from your backend server
        console.log("Login successful, backend response:", data);
        setUserInfo(data);
      })
      .catch((error) => {
        // Handle errors in communicating with your backend server
        console.error("Error exchanging authorization code:", error);
      });
  };

  const handleError = (errorResponse) => {
    console.error("Google login failed", errorResponse);
  };
  const login = useGoogleLogin({
    onSuccess: handleSuccess,
    onError: handleError,
    flow: "auth-code",
  });
  return (
    <div>
      <button onClick={() => login()}>Sign in with Google 🚀</button>
    </div>
  );
};
