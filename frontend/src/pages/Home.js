import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <h1 className="mb-5 text-white"> Welcome to Consulting Booking System!</h1>

      <div className="landing-row">

        {/* CLIENT COLUMN */}
        <div className="consultant-column">

          {/* Client Login Box */}
          <div className="landing-box client-box">
            <div className="landing-card-body">
              <h2>Client</h2>
              <p>If you are a client, click the button below.</p>
              <button className="btn btn-light" onClick={() => navigate("/client-login")}>Client Login</button>
            </div>
          </div>

          {/* Client Signup Box */}
          <div className="landing-box signup-box client-signup">
            <div className="landing-card-body">
              <p>New Client?</p>
              <button className="btn btn-light" onClick={() => navigate("/client-signup")}>Sign Up</button>
            </div>
          </div>

        </div>

        {/* CONSULTANT COLUMN */}
        <div className="consultant-column">

          {/* Consultant Login Box */}
          <div className="landing-box consultant-box">
            <div className="landing-card-body">
              <h2>Consultant</h2>
              <p>If you are a consultant, click the button below.</p>
              <button className="btn btn-light"onClick={() => navigate("/consultant-login")}>Consultant Login</button>
            </div>
          </div>

          {/* Consultant Signup Box */}
          <div className="landing-box signup-box consultant-signup">
            <div className="landing-card-body">
              <p>New Consultant?</p>
              <button className="btn btn-light" onClick={() => navigate("/consultant-signup")}>Sign Up</button>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}

export default Home;