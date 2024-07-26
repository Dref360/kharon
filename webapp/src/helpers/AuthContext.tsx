import { useEffect, useState } from "react";
import { callIsLoggedIn, callLogout } from "../api/api";

export const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuthStatus = async () => {
    setIsLoading(true);
    await callIsLoggedIn().then((response) => setIsLoggedIn(!!response));
  };

  const logout = async () => {
    await callLogout().then((res) => setIsLoggedIn(!res))
  }

  useEffect(() => {
    async function fetchAuthStatus() {
      await checkAuthStatus();
      setIsLoading(false);
    }
    fetchAuthStatus();
  }, []);

  return { isLoggedIn, isLoading, logout };
};
