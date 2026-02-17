import { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Login.css'; // We'll create this for basic styling

export default function Login() {
  const { login, error } = useAuth();
  const [loading, setLoading] = useState(false);
  const [loginError, setLoginError] = useState('');

  async function handleLogin() {
    try {
      setLoginError('');
      setLoading(true);
      await login();
    } catch (err) {
      setLoginError('Failed to log in: ' + err.message);
    }
    setLoading(false);
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <h2>Dundra ADK Login</h2>
        {error && <div className="error-message">{error}</div>}
        {loginError && <div className="error-message">{loginError}</div>}
        <button onClick={handleLogin} disabled={loading} className="login-btn">
          Sign in with Google
        </button>
      </div>
    </div>
  );
}
