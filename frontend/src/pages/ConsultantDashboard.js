import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // for navigation
import { getConsultantBookings } from "../services/api";
import { confirmBooking, rejectBooking } from "../services/api";
import "./ConsultantDashboard.css";

export default function ConsultantDashboard() {
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const consultantId = localStorage.getItem("consultant_id") || "consultant1"; // Get logged-in consultant ID

  useEffect(() => {
    async function fetchBookings() {
      try {
        const data = await getConsultantBookings(consultantId);
        console.log("Fetched bookings:", data); // check what comes here in testing 
        setBookings(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    fetchBookings();
  }, [consultantId]);

  async function handleAccept(bookingId) {
  try {
    await confirmBooking(bookingId);

    // update UI instantly (no refresh needed)
    setBookings((prev) =>
      prev.map((b) =>
        b.booking_id === bookingId ? { ...b, state: "CONFIRMED" } : b
      )
    );
  } catch (err) {
    console.error(err);
  }
}

async function handleReject(bookingId) {
  try {
    await rejectBooking(bookingId);

    setBookings((prev) =>
      prev.map((b) =>
        b.booking_id === bookingId ? { ...b, state: "REJECTED" } : b
      )
    );
  } catch (err) {
    console.error(err);
  }
}

  if (loading) {
    return (
      <div className="consultant-dashboard d-flex justify-content-center align-items-center vh-100">
        Loading bookings...
      </div>
    );
  }

  return (
    <div className="consultant-dashboard container mt-4">
      <h1 className="text-center mb-4">Consultant Dashboard</h1>

      <div className="mb-3 text-center">
        <button
          className="btn btn-primary me-2"
          onClick={() => navigate("/manage-timeslots")}
        >
          Manage Timeslots
        </button>

        <button
          className="btn btn-primary me-2"
          onClick={() => navigate("/manage-services")}
        >
          Manage Services
        </button>
      </div>

      <div className="table-responsive">
        <table className="table table-bordered table-hover">
          <thead className="table-dark">
            <tr>
              <th>Booking ID</th>
              <th>Client Name</th>
              <th>Service</th>
              <th>Start Time</th>
              <th>End Time</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {bookings.length === 0 ? (
              <tr>
                <td colSpan="7" className="text-center">
                  No bookings available
                </td>
              </tr>
            ) : (
              bookings.map((b) => (
                <tr key={b.booking_id}>
                  <td>{b.booking_id}</td>
                  <td>{b.client_name}</td>
                  <td>{b.service_name}</td>
                  <td>{new Date(b.start_time).toLocaleString()}</td>
                  <td>{new Date(b.end_time).toLocaleString()}</td>
                  <td>
                    <span
                      className={
                        b.state === "CONFIRMED"
                          ? "text-success"
                          : b.state === "REJECTED"
                          ? "text-danger"
                          : "text-warning"
                      }
                    >
                      {b.state}
                    </span>
                  </td>
                  {/* ACTION BUTTONS */}
                  <td>
                    {b.state === "PENDING" && (
                      <>
                        <button
                          className="btn btn-success btn-sm me-2"
                          onClick={() => handleAccept(b.booking_id)}
                        >
                          Accept
                        </button>

                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleReject(b.booking_id)}
                        >
                          Reject
                        </button>
                      </>
                    )}
                </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}