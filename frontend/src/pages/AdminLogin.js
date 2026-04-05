import { useState } from "react";
import "./ConsultantLogin.css";

export default function AdminLogin() {
  const [user_id, setUserId] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:5000/api/admin/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ user_id, password })
      });

      const data = await res.json();

      if (data.success) {
        console.log("Admin logged in:", data);
        window.location.href = "/admin-dashboard";
      } else {
        alert(data.message);
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