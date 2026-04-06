import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPayments } from "../services/api";

export default function PaymentPage() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchPayments() {
      try {
        const data = await getPayments(clientId);
        setPayments(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    if (clientId) {
      fetchPayments();
    }
  }, [clientId]);

  if (loading) {
    return <div className="text-center mt-5">Loading payments...</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Payments</h2>

      <button onClick={() => navigate(-1)} className="btn btn-secondary mb-3">
        Back
      </button>

      {payments.length === 0 ? (
        <p>No payments found</p>
      ) : (
        payments.map((p) => (
          <div key={p.payment_id || p.id} style={{ marginBottom: "10px", padding: "10px", border: "1px solid #ccc" }}>
            <p><strong>Amount:</strong> ${p.amount}</p>
            <p><strong>Status:</strong> {p.status}</p>
            <p><strong>Date:</strong> {p.created_at}</p>
          </div>
        ))
      )}
    </div>
  );
}