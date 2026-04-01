import { useNavigate } from "react-router-dom";
import "./Home.css";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <h1 className="mb-5 text-white">Welcome!</h1>

      <div className="landing-row">
        {/* Client Box */}
        <div className="landing-box client-box">
          <div className="landing-card-body">
            <h2>Client</h2>
            <p>If you are a client, click the button below.</p>
            <button className="btn btn-light" onClick={() => navigate("/client-login")}>Client Login</button>
          </div>
        </div>

        {/* Consultant Box */}
        <div className="landing-box consultant-box">
          <div className="landing-card-body">
            <h2>Consultant</h2>
            <p>If you are a consultant, click the button below.</p>
            <button className="btn btn-light" onClick={() => navigate("/consultant-login")}>Consultant Login</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;