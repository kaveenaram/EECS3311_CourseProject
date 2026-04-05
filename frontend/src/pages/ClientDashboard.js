import { useNavigate } from "react-router-dom";

export default function ClientDashboard() {
  const navigate = useNavigate();


  
  return (
    <div style={{ padding: "20px" }}>
      <h1>Client Dashboard</h1>

      <button onClick={() => navigate("/services")}>
        Browse Services
      </button>

      <button onClick={() => navigate("/bookings")}>
        Booking History
      </button>

      <button onClick={() => navigate("/payments")}>
        Payments
      </button>
    </div>
  );


}