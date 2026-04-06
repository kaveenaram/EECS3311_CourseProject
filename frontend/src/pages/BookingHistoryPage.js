import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getClientBookings, cancelBooking } from "../services/api";

export default function BookingHistoryPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cancellationError, setCancellationError] = useState(null);
  const navigate = useNavigate();
  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchBookings() {
      if (!clientId) {
        setError("You must be logged in to view your bookings.");
        setLoading(false);
        return;
      }

      try {
        setError(null);
        const data = await getClientBookings(clientId);
        
        if (!data || !Array.isArray(data) || data.length === 0) {
          setError("You don't have any bookings yet. Start by browsing our services!");
          setBookings([]);
        } else {
          setBookings(data);
        }
        setLoading(false);
      } catch (err) {
        console.error("Error fetching bookings:", err);
        setError("Failed to load your bookings. Please try again later.");
        setLoading(false);
      }
    }
    fetchBookings();
  }, [clientId]);

  async function handleCancel(bookingId) {
    if (!bookingId) {
      setCancellationError("Invalid booking selected.");
      return;
    }

    if (!window.confirm("Are you sure you want to cancel this booking?")) {
      return;
    }

    try {
      setCancellationError(null);
      const result = await cancelBooking(bookingId);
      
      if (result.success) {
        setBookings(bookings.filter(b => b.booking_id !== bookingId));
        alert("Booking cancelled successfully");
      } else {
        setCancellationError(result.message || "Failed to cancel booking. Please try again.");
      }
    } catch (err) {
      console.error("Error cancelling booking:", err);
      setCancellationError("An error occurred while cancelling. Please try again.");
    }
  }

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <p>Loading your bookings...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-info" role="alert">
          <h4 className="alert-heading">No Bookings Found</h4>
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
      <h2>Your Booking History</h2>

      <button onClick={() => navigate("/client-dashboard")} className="btn btn-secondary mb-3">
        Back
      </button>

      {cancellationError && (
        <div className="alert alert-danger" role="alert">
          {cancellationError}
        </div>
      )}

      {bookings.length === 0 ? (
        <div className="alert alert-info">
          <p>You don't have any bookings yet.</p>
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
                <th>Booking ID</th>
                <th>Service</th>
                <th>Consultant</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {bookings.map((b) => (
                <tr key={b.booking_id}>
                  <td>{b.booking_id}</td>
                  <td>{b.service_id}</td>
                  <td>{b.consultant_id}</td>
                  <td>
                    <span className={`badge ${b.state === 'CONFIRMED' ? 'bg-success' : b.state === 'CANCELLED' ? 'bg-danger' : 'bg-warning'}`}>
                      {b.state}
                    </span>
                  </td>
                  <td>{b.created_at ? new Date(b.created_at).toLocaleDateString() : "N/A"}</td>
                  <td>
                    {b.state !== 'CANCELLED' && b.state !== 'COMPLETED' && (
                      <button 
                        onClick={() => handleCancel(b.booking_id)}
                        className="btn btn-danger btn-sm"
                      >
                        Cancel
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
  );
}