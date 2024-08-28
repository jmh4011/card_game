import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
import { RecoilRoot } from "recoil";
import { CookiesProvider } from "react-cookie";
import { BrowserRouter } from "react-router-dom";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
root.render(
  <BrowserRouter>
    <RecoilRoot>
      <CookiesProvider>
        <React.StrictMode>
          <App />
        </React.StrictMode>
      </CookiesProvider>
    </RecoilRoot>
  </BrowserRouter>
);
