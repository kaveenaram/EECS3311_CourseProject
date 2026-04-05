import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "./AdminDashboard.css";

export default function AdminDashboard() {
  const [consultants, setConsultants] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://localhost:5000/api/admin/consultants")
      .then(res => res.json())
      .then(data => {
        setConsultants(data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  async function approveConsultant(id) {
    try {
      await fetch(`http://localhost:5000/api/admin/approve/${id}`, {
        method: "POST"
      });
      setConsultants(prev =>
        prev.map(c => (c.user_id === id ? { ...c, approved: true } : c))
      );
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
                      onClick={() => approveConsultant(c.user_id)}
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