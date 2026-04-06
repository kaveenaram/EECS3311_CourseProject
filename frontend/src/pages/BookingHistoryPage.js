import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getClientBookings, cancelBooking } from "../services/api";

export default function BookingHistoryPage() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchBookings() {
      try {
        const data = await getClientBookings(clientId);
        setBookings(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    if (clientId) {
      fetchBookings();
    }
  }, [clientId]);

  async function handleCancel(bookingId) {
    try {
      await cancelBooking(bookingId);
      setBookings(bookings.filter(b => b.booking_id !== bookingId));
      alert("Booking cancelled");
    } catch (err) {
      console.error(err);
      alert("Failed to cancel booking");
    }
  }

  if (loading) {
    return <div className="text-center mt-5">Loading bookings...</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Booking History</h2>

      <button onClick={() => navigate(-1)} className="btn btn-secondary mb-3">
        Back
      </button>

      {bookings.length === 0 ? (
        <p>No bookings found</p>
      ) : (
        bookings.map((b) => (
          <div key={b.booking_id} style={{ marginBottom: "10px", padding: "10px", border: "1px solid #ccc" }}>
            <p><strong>Service:</strong> {b.service_id}</p>
            <p><strong>Consultant:</strong> {b.consultant_id}</p>
            <p><strong>Status:</strong> {b.state}</p>
            <p><strong>Date:</strong> {b.created_at}</p>
            {b.state !== "CANCELLED" && (
              <button 
                onClick={() => handleCancel(b.booking_id)}
                className="btn btn-danger btn-sm"
              >
                Cancel
              </button>
            )}
          </div>
        ))
      )}
    </div>
  );
}