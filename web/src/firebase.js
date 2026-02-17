import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

let app;
let auth;

export const initFirebase = (config) => {
  if (!app) {
    app = initializeApp(config);
    auth = getAuth(app);
  }
  return app;
};

export { auth };
