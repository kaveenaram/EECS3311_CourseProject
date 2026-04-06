import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultants, approveConsultant, getAllPayments, getAllBookings } from "../services/api";
import "./AdminDashboard.css";

export default function AdminDashboard() {
  const [consultants, setConsultants] = useState([]);
  const [allBookings, setAllBookings] = useState([]);
  const [allPayments, setAllPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("consultants"); // "consultants", "bookings", "payments"
  const [error, setError] = useState(null);
  const adminId = localStorage.getItem("admin_id") || "admin1";
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchAdminData() {
      try {
        setError(null);
        setLoading(true);
        
        const [consultantsData, bookingsData, paymentsData] = await Promise.all([
          getConsultants(),
          getAllBookings(adminId),
          getAllPayments(adminId)
        ]);
        
        setConsultants(consultantsData || []);
        setAllBookings(bookingsData || []);
        setAllPayments(paymentsData || []);
      } catch (err) {
        console.error("Error fetching admin data:", err);
        setError("Failed to load admin data");
      } finally {
        setLoading(false);
      }
    }
    
    if (adminId) {
      fetchAdminData();
    }
  }, [adminId]);

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
      setError("Failed to approve consultant");
    }
  }

  if (loading) {
    return (
      <div className="admin-dashboard text-center mt-5">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  return (
    <div className="admin-dashboard" style={{ padding: "20px" }}>
      <h1>Admin Dashboard</h1>

      {error && (
        <div className="alert alert-danger" role="alert">
          {error}
        </div>
      )}

      <div className="mb-3 d-flex gap-2 align-items-center">
        <button className="btn btn-primary" onClick={() => navigate("/admin/policies")}>
          Manage Policies
        </button>
        <button 
          className="btn btn-outline-secondary" 
          onClick={() => window.location.reload()}
        >
          Refresh
        </button>
      </div>

      {/* Tab Navigation */}
      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === "consultants" ? "active" : ""}`}
            onClick={() => setActiveTab("consultants")}
          >
            Consultants {consultants.length > 0 && `(${consultants.length})`}
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === "bookings" ? "active" : ""}`}
            onClick={() => setActiveTab("bookings")}
          >
            All Bookings {allBookings.length > 0 && `(${allBookings.length})`}
          </button>
        </li>
        <li className="nav-item">
          <button
            className={`nav-link ${activeTab === "payments" ? "active" : ""}`}
            onClick={() => setActiveTab("payments")}
          >
            All Payments {allPayments.length > 0 && `(${allPayments.length})`}
          </button>
        </li>
      </ul>

      {/* Consultants Tab */}
      {activeTab === "consultants" && (
        <div>
          <h3 className="mb-3">Pending Consultant Approvals</h3>
          {consultants.length === 0 ? (
            <div className="alert alert-info">No consultants found</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered table-hover">
                <thead className="table-dark">
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>User ID</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {consultants.map(c => (
                    <tr key={c.user_id}>
                      <td>{c.name}</td>
                      <td>{c.email}</td>
                      <td>{c.user_id}</td>
                      <td>
                        <span className={`badge ${c.approved ? "bg-success" : "bg-warning"}`}>
                          {c.approved ? "Approved" : "Pending"}
                        </span>
                      </td>
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
          )}
        </div>
      )}

      {/* Bookings Tab */}
      {activeTab === "bookings" && (
        <div>
          <h3 className="mb-3">All Bookings</h3>
          {allBookings.length === 0 ? (
            <div className="alert alert-info">No bookings found</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered table-hover table-sm">
                <thead className="table-dark">
                  <tr>
                    <th>Booking ID</th>
                    <th>Client ID</th>
                    <th>Consultant ID</th>
                    <th>Service ID</th>
                    <th>State</th>
                    <th>Created</th>
                  </tr>
                </thead>
                <tbody>
                  {allBookings.map(b => (
                    <tr key={b.booking_id}>
                      <td>{b.booking_id}</td>
                      <td>{b.client_id}</td>
                      <td>{b.consultant_id}</td>
                      <td>{b.service_id}</td>
                      <td>
                        <span className={`badge ${
                          b.state === 'CONFIRMED' ? 'bg-success' :
                          b.state === 'CANCELLED' ? 'bg-danger' :
                          b.state === 'COMPLETED' ? 'bg-info' :
                          'bg-warning'
                        }`}>
                          {b.state}
                        </span>
                      </td>
                      <td>{b.created_at ? new Date(b.created_at).toLocaleDateString() : "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}

      {/* Payments Tab */}
      {activeTab === "payments" && (
        <div>
          <h3 className="mb-3">All Payments</h3>
          {allPayments.length === 0 ? (
            <div className="alert alert-info">No payments found</div>
          ) : (
            <div className="table-responsive">
              <table className="table table-bordered table-hover table-sm">
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
                  {allPayments.map(p => (
                    <tr key={p.payment_id || p.booking_id}>
                      <td>{p.payment_id}</td>
                      <td>{p.booking_id}</td>
                      <td>${parseFloat(p.amount).toFixed(2)}</td>
                      <td>
                        <span className={`badge ${p.status === 'COMPLETED' ? 'bg-success' : 'bg-danger'}`}>
                          {p.status}
                        </span>
                      </td>
                      <td>{p.timestamp ? new Date(p.timestamp).toLocaleDateString() : "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}