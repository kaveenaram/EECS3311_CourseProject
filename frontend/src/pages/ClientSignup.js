import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signupClient } from "../services/api";
import "./Client.css";

function ClientSignup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    user_id: "",
    name: "",
    email: "",
    password: ""
  });

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSignup() {
    const res = await signupClient(form);
    if (res.success) {
      alert("Account created! You can now login.");
      navigate("/client-login");
    } else {
      alert(res.message || "Signup failed");
    }
  }

  return (
    <div className="full-page">
      <div className="login-box">
        <h2>Client Signup</h2>

        <input name="user_id" placeholder="User ID" onChange={handleChange} />
        <input name="name" placeholder="Name" onChange={handleChange} />
        <input name="email" placeholder="Email" onChange={handleChange} />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} />

        <button onClick={handleSignup}>Sign Up</button>
      </div>
    </div>
  );
}

export default ClientSignup;
