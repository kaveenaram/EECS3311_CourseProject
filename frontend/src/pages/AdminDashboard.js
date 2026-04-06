import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultants, approveConsultant } from "../services/api";
import "./AdminDashboard.css";

export default function AdminDashboard() {
  const [consultants, setConsultants] = useState([]);
  const [loading, setLoading] = useState(true);
  const adminId = localStorage.getItem("admin_id") || "admin1"; // Get logged-in admin ID
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchConsultants() {
      const data = await getConsultants();
      setConsultants(data);
      setLoading(false);
    }
    fetchConsultants();
  }, []);

  async function handleApprove(id) {
    try {
      const res = await approveConsultant(id, adminId);
      if (res.success) {
        setConsultants(prev =>
          prev.map(c => (c.user_id === id ? { ...c, approved: true } : c))
        );
      }
    } catch (err) {
      console.error(err);
    }
  }

  if (loading) {
    return <div className="admin-dashboard text-center">Loading consultants...</div>;
  }

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard</h1>

      <div className="mb-3" align="center">
        <button className="btn btn-primary" onClick={() => navigate("/admin/policies")}> Manage Policies</button>
      </div>

      <div className="table-responsive">
        <table className="table table-bordered table-hover">
          <thead className="table-dark">
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {consultants.map(c => (
              <tr key={c.user_id}>
                <td>{c.name}</td>
                <td>{c.email}</td>
                <td>{c.approved ? "Approved" : "Pending"}</td>
                <td>
                  {!c.approved && (
                    <button
                      className="btn btn-success btn-sm"
                      onClick={() => handleApprove(c.user_id)}
                    >
                      Approve
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}