import React from 'react';
import ReactDOM from "react-dom/client";
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './App';
const GOOGLE_ACCESS_KEY = process.env.REACT_APP_GOOGLE_CLIENT_ID || '';
const root = ReactDOM.createRoot(document.getElementById("root") as HTMLElement);

root.render(
  (<React.StrictMode>
    <GoogleOAuthProvider clientId={GOOGLE_ACCESS_KEY}>
      <App />
    </GoogleOAuthProvider>
  </React.StrictMode>)
);