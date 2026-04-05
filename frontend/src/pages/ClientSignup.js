import { useNavigate } from "react-router-dom";
import "./ConsultantSignup.css";

function ClientSignup() {
  const navigate = useNavigate();

  function handleSignup() {
    // No backend yet → just redirect
    alert("Signup successful!");
    navigate("/client-login");
  }

  return (
    <div className="full-page">
      <div className="login-box">
        <h2 className="title">Client Sign Up</h2>

        <input placeholder="Full Name" />
        <input placeholder="Email" />
        <input placeholder="Username" />
        <input type="password" placeholder="Password" />

        <button onClick={handleSignup}>
          Create Account
        </button>

        <div className="login-link">
          Already have an account?{" "}
          <span onClick={() => navigate("/client-login")}>
            Login
          </span>
        </div>
      </div>
    </div>
  );

  
}

export default ClientSignup;
