import { useEffect, useState } from "react";

export const useAuth = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const checkAuthStatus = async () => {
    setIsLoading(true)
    return await fetch("/app/me", { credentials: "include" })
      .then((res) => setIsLoggedIn(res.ok))
      .catch(() => setIsLoggedIn(false));
  };

  const logout = async () => {
    try {
      const response = await fetch(`/auth/logout`, {
        method: 'POST',
        credentials: 'include',
      });
      if (!response.ok) {
        throw new Error('Logout failed');
      }
      setIsLoggedIn(false)
      return await response.json();
    } catch (error) {
      console.error('Error during logout:', error);
      throw error;
    }
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
