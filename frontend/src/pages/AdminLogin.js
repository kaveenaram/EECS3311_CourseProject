import { useState } from "react";
import { loginAdmin } from "../services/api";
import "./ConsultantLogin.css";

export default function AdminLogin() {
  const [user_id, setUserId] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const data = await loginAdmin(user_id, password);

      if (data.success) {
        console.log("Admin logged in:", data);
        window.location.href = "/admin-dashboard";
      } else {
        alert("Invalid credentials");
      }
    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  }

  return (
    <div className="full-page">
      <form className="login-box" onSubmit={handleSubmit}>
        <h2 style={{ textAlign: "center", color: "white", marginBottom: "20px" }}>
          Admin Login
        </h2>

        <input
          type="text"
          placeholder="User ID"
          value={user_id}
          onChange={(e) => setUserId(e.target.value)}
          required
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="btn btn-light mt-3" type="submit">Login</button>
      </form>
    </div>
  );
}