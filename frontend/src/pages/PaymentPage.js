import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPayments } from "../services/api";

export default function PaymentPage() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchPayments() {
      if (!clientId) {
        setError("You must be logged in to view your payment history.");
        setLoading(false);
        return;
      }

      try {
        setError(null);
        const data = await getPayments(clientId);
        
        if (!data || !Array.isArray(data) || data.length === 0) {
          setError("You don't have any payments yet. Start by booking a service!");
          setPayments([]);
        } else {
          setPayments(data);
        }
        setLoading(false);
      } catch (err) {
        console.error("Error fetching payments:", err);
        setError("Failed to load your payment history. Please try again later.");
        setLoading(false);
      }
    }
    fetchPayments();
  }, [clientId]);

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <p>Loading your payment history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-info" role="alert">
          <h4 className="alert-heading">No Payments Found</h4>
          <p>{error}</p>
          <button 
            onClick={() => navigate("/client-dashboard")} 
            className="btn btn-primary mt-2"
          >
            Browse Services
          </button>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Payment History</h2>

      <button onClick={() => navigate("/client-dashboard")} className="btn btn-secondary mb-3">
        Back
      </button>

      {payments.length === 0 ? (
        <div className="alert alert-info">
          <p>You don't have any payments yet.</p>
          <button 
            onClick={() => navigate("/client-dashboard")} 
            className="btn btn-primary mt-2"
          >
            Start Booking
          </button>
        </div>
      ) : (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead className="table-dark">
              <tr>
                <th>Payment ID</th>
                <th>Booking ID</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((p) => (
                <tr key={p.payment_id || p.id}>
                  <td>{p.payment_id || p.id}</td>
                  <td>{p.booking_id}</td>
                  <td>${p.amount ? parseFloat(p.amount).toFixed(2) : "0.00"}</td>
                  <td>
                    <span className={`badge ${p.status === 'COMPLETED' ? 'bg-success' : p.status === 'FAILED' ? 'bg-danger' : 'bg-warning'}`}>
                      {p.status}
                    </span>
                  </td>
                  <td>{p.created_at ? new Date(p.created_at).toLocaleDateString() : "N/A"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}