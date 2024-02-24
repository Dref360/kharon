import { GoogleOAuthProvider } from "@react-oauth/google";
import { useEffect, useState } from "react";
import "./App.css";
import {
  GoogleSignIn,
  UserInfoProvider,
  useUserInfoContext,
} from "./components/GoogleSignIn";
import logo from "./logo.svg";

const BACKEND_URL = "http://0.0.0.0:8000";
const GOOGLE_ACCESS_KEY = "590400439644-il4durbc07c0dii1isin8lbbqpmdienp.apps.googleusercontent.com"

const Greeting = () => {
  const { userInfo } = useUserInfoContext();
  return <p>Hello {userInfo?.name || "Unknown"}</p>;
};

const UserData = () => {
  const { credential } = useUserInfoContext();
  const [userData, setUserData] = useState(null);

  useEffect(() => {
    async function getData() {
      if (credential) {
        const userInfo = await fetch(
          `${BACKEND_URL}/api/userData?credentials=${credential}`
        ).then((res) => res.json());
        setUserData(userInfo.data);
      }
    }
    getData();
    return () => {
      // this now gets called when the component unmounts
    };
  }, [credential]);
  return <p>Hello {userData?.username}</p>;
};

function App() {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_ACCESS_KEY}>
      <UserInfoProvider>
        <div className="App">
          <header className="App-header">
            <img src={logo} className="App-logo" alt="logo" />
            <Greeting />
            <UserData />
            <GoogleSignIn />
            <a
              className="App-link"
              href="https://reactjs.org"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn React
            </a>
          </header>
        </div>
      </UserInfoProvider>
    </GoogleOAuthProvider>
  );
}

export default App;
