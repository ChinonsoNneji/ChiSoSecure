import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Shield } from "lucide-react";

import api from "../api";

function Login() {
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    const body = new URLSearchParams();
    body.append("username", username);
    body.append("password", password);

    try {
      const response = await api.post(
        "/auth/login",
        body,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

      localStorage.setItem(
        "chisosecure_token",
        response.data.access_token
      );

      navigate("/");
    } catch {
      setError("Incorrect username or password.");
    }
  }

  return (
    <div className="login-page">
      <div className="login-shell">
        <div className="login-brand">
          <div className="brand-icon">
            <Shield size={19} />
          </div>

          <span>ChiSoSecure</span>
        </div>

        <div className="login-copy">
          <p className="eyebrow">Security Operations</p>
          <h1>Sign in</h1>
          <p>
            Access the ChiSoSecure operations console.
          </p>
        </div>

        <form
          className="login-form"
          onSubmit={handleSubmit}
        >
          <label>
            Username
            <input
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              required
            />
          </label>

          {error && (
            <div className="login-error">
              {error}
            </div>
          )}

          <button type="submit" className="login-button">
            Continue
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;