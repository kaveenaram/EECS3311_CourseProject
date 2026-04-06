import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signupConsultant } from "../services/api";
import "./ConsultantSignup.css";

function ConsultantSignup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    user_id: "",
    name: "",
    email: "",
    password: ""
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  }

    async function handleSubmit(e) {
    e.preventDefault();

    try {
      const data = await signupConsultant(form);

      if (data.success) {
        alert("Signup successful! Waiting for admin approval.");
        navigate("/consultant-login");
      } else {
        alert(data.message || "Signup failed");
      }
    } catch (err) {
      console.error(err);
      alert("Server error");
    }
  }

  return (
    <div className="full-page">
      <form className="login-box" onSubmit={handleSubmit}>
        <h2 className="title">Consultant Signup</h2>

        <input
          type="text"
          name="user_id"
          placeholder="User ID"
          value={form.user_id}
          onChange={handleChange}
          required
        />

        <input
          type="text"
          name="name"
          placeholder="Full Name"
          value={form.name}
          onChange={handleChange}
          required
        />

        <input
          type="email"
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          required
        />

        <button type="submit">Sign Up</button>

        <p className="login-link">
          Already approved?{" "}
          <span onClick={() => navigate("/consultant-login")}>
            Login here
          </span>
        </p>
      </form>
    </div>
  );
}

export default ConsultantSignup;