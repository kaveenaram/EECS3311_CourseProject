import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getPolicies, updatePolicies } from "../services/api";

export default function AdminPolicies() {
  const navigate = useNavigate();
  const adminId = localStorage.getItem("admin_id") || "admin1";
  const [policies, setPolicies] = useState({
    cancellationRules: "",
    pricingStrategy: "",
    refundPolicy: ""
  });

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPolicies() {
      try {
        const data = await getPolicies(adminId);
        setPolicies({
          cancellationRules: data.cancellation_rules || "",
          pricingStrategy: data.pricing_strategy || "",
          refundPolicy: data.refund_policy || ""
        });
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    fetchPolicies();
  }, [adminId]);

  async function handleUpdatePolicies(e) {
    e.preventDefault();

    try {
      const result = await updatePolicies(adminId, policies);
      if (result.success) {
        alert("Policies updated!");
      }
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

      <form onSubmit={handleUpdatePolicies}>
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