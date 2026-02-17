import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import { initFirebase } from './firebase.js'

async function initAndRender() {
  try {
    const response = await fetch('/api/config');
    if (!response.ok) throw new Error('Failed to load config');
    const config = await response.json();
    initFirebase(config);
  } catch (e) {
    console.error("Failed to initialize Firebase:", e);
    // You might want to render an error screen here
  }

  createRoot(document.getElementById('root')).render(
    <StrictMode>
      <App />
    </StrictMode>,
  )
}

initAndRender();
