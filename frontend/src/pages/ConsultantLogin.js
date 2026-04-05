import React, { useState } from "react";
import { loginConsultant } from "../services/api"; 
import "./ConsultantLogin.css";

const ConsultantLogin = ({ onLoginSuccess }) => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await loginConsultant(userId, password);

      if (response.success) {
        // Pass the consultant data to the dashboard or parent component
        onLoginSuccess(response.consultant);
      } else {
        setError("Invalid credentials. Please try again.");
      }
    } catch (err) {
      console.error(err);
      setError("Server error. Please try again later.");
    }
  };

  return (
    <div className="full-page">
      <div className="login-box">
        <h2 style={{ color: "#fff", textAlign: "center", marginBottom: "20px" }}>
          Consultant Login
        </h2>
        {error && <p style={{ color: "red", textAlign: "center" }}>{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="User ID"
            value={userId}
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
          <button className="btn btn-light mt-3" type="submit">Log In</button>
        </form>
      </div>
    </div>
  );
};

export default ConsultantLogin;