import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function AdminPolicies() {
  const navigate = useNavigate();
  const [policies, setPolicies] = useState({
    cancellationRules: "",
    pricingStrategy: "",
    refundPolicy: ""
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:5000/api/admin/get-policies")
      .then(res => res.json())
      .then(data => {
        setPolicies(data);
        setLoading(false);
      })
      .catch(err => console.error(err));
  }, []);

  async function updatePolicies(e) {
    e.preventDefault();

    try {
      await fetch("http://localhost:5000/api/admin/update-policy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cancellation_rules: policies.cancellationRules,
          pricing_strategy: policies.pricingStrategy,
          refund_policy: policies.refundPolicy
        })
      });
      alert("Policies updated!");
    } catch (err) {
      console.error(err);
    }
  }

  if (loading)
    return (
      <div className="d-flex justify-content-center align-items-center vh-100">
        Loading policies...
      </div>
    );

 return (
  <div className="d-flex justify-content-center align-items-center vh-100">
    <div className="w-100" style={{ maxWidth: "600px" }}>
      <h2 className="text-center mb-4">Manage System Policies</h2>

      {/* Back Button */}
      <div className="mb-3" align="center">
        <button 
          className="btn btn-secondary"
          onClick={() => navigate("/admin-dashboard")} // path to your dashboard
        >
          ← Back to Dashboard
        </button>
      </div>

      <form onSubmit={updatePolicies}>
        <div className="mb-3">
          <label className="form-label">Cancellation Rules</label>
          <textarea
            className="form-control"
            value={policies.cancellationRules}
            onChange={e =>
              setPolicies({ ...policies, cancellationRules: e.target.value })
            }
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Pricing Strategy</label>
          <textarea
            className="form-control"
            value={policies.pricingStrategy}
            onChange={e =>
              setPolicies({ ...policies, pricingStrategy: e.target.value })
            }
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Refund Policy</label>
          <textarea
            className="form-control"
            value={policies.refundPolicy}
            onChange={e =>
              setPolicies({ ...policies, refundPolicy: e.target.value })
            }
          />
        </div>
        <div className="text-center">
          <button className="btn btn-success" type="submit">
            Update Policies
          </button>
        </div>
      </form>
    </div>
  </div>
);
}