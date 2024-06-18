import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { RecoilRoot } from 'recoil';
import {CookiesProvider} from 'react-cookie';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <RecoilRoot>
    <CookiesProvider>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </CookiesProvider>
  </RecoilRoot>
);

reportWebVitals();
