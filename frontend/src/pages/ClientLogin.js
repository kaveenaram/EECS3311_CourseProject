import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { loginClient } from "../services/api";
import "./Client.css";

function ClientLogin() {
  const [user_id, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  async function handleLogin() {
    const res = await loginClient(user_id, password);

    if (res.success) {
      localStorage.setItem("client_id", user_id);
      navigate("/client-dashboard");
    } else {
      alert("Invalid login");
    }
  }

  return (
    <div className="full-page">
      <div className="login-box">
        <h2>Client Login</h2>

        <input placeholder="User ID" onChange={e => setUserId(e.target.value)} />
        <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />

        <button onClick={handleLogin}>Login</button>
      </div>
    </div>
  );
}

export default ClientLogin;
