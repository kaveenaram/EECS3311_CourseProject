import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getServices, getAvailableSlots, bookService, getClientBookings, cancelBooking } from "../services/api";
import "./Client.css";

function ClientDashboard() {
  const [services, setServices] = useState([]);
  const [slots, setSlots] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [bookingError, setBookingError] = useState(null);
  const [slotsLoading, setSlotsLoading] = useState(false);
  const [bookings, setBookings] = useState([]);
  const [bookingsLoading, setBookingsLoading] = useState(false);
  const [cancellationError, setCancellationError] = useState(null);
  const navigate = useNavigate();

  const clientId = localStorage.getItem("client_id");

  async function fetchServices() {
    try {
      setError(null);
      const data = await getServices();
      
      if (!data || data.length === 0) {
        setError("No services available at this time. Please try again later.");
        setServices([]);
      } else {
        setServices(data);
      }
      setLoading(false);
    } catch (err) {
      console.error("Error fetching services:", err);
      setError("Failed to load services. Please refresh the page.");
      setLoading(false);
    }
  }

  async function fetchBookings() {
    if (!clientId) {
      return;
    }
    setBookingsLoading(true);
    try {
      const data = await getClientBookings(clientId);
      setBookings(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Error fetching bookings:", err);
      setBookings([]);
    }
    setBookingsLoading(false);
  }

  useEffect(() => {
    fetchServices();
    fetchBookings();
  }, [clientId]);

  async function handleRefresh() {
    setLoading(true);
    await fetchServices();
    await fetchBookings();
  }

  async function selectService(service) {
    if (!service || !service.consultant_id) {
      setBookingError("Invalid service selected. Please try again.");
      return;
    }

    try {
      setSlotsLoading(true);
      setBookingError(null);
      setSelectedService(service);
      
      const fetchedSlots = await getAvailableSlots(service.consultant_id, service.service_id);
      
      if (!fetchedSlots || fetchedSlots.length === 0) {
        setBookingError("No available time slots for this service. Please try another service.");
        setSlots([]);
      } else {
        setSlots(fetchedSlots);
      }
      setSlotsLoading(false);
    } catch (err) {
      console.error("Error fetching available slots:", err);
      setBookingError("Failed to load available times. Please try again.");
      setSlotsLoading(false);
    }
  }

  async function handleBooking(slot) {
    if (!slot || !slot.slot_id) {
      setBookingError("Invalid time slot selected.");
      return;
    }

    if (!selectedService || !selectedService.service_id) {
      setBookingError("Invalid service selected.");
      return;
    }

    if (!clientId) {
      setBookingError("You must be logged in to book a service.");
      return;
    }

    try {
      const result = await bookService({
        client_id: clientId,
        consultant_id: selectedService.consultant_id,
        service_id: selectedService.service_id,
        slot_id: slot.slot_id
      });

      if (result.success) {
        alert("Booking successful!");
        setSelectedService(null);
        setSlots([]);
        await fetchBookings();
      } else {
        setBookingError(result.message || "Failed to book service. Please try again.");
      }
    } catch (err) {
      console.error("Booking error:", err);
      setBookingError("An error occurred while booking. Please try again.");
    }
  }

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
        <p>Loading available services...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <div className="alert alert-warning" role="alert">
          <h4 className="alert-heading">No Services Available</h4>
          <p>{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="btn btn-primary mt-2"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Client Dashboard</h1>
        <div className="gap-2">
          <button 
            onClick={handleRefresh} 
            className="btn btn-warning me-2"
          >
            Refresh
          </button>
          <button 
            onClick={() => navigate("/payment-management")} 
            className="btn btn-info me-2"
          >
            Payments
          </button>
          <button 
            onClick={() => navigate("/")} 
            className="btn btn-secondary"
          >
            Back
          </button>
        </div>
      </div>

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Your Current Bookings</h5>
          {cancellationError && (
            <div className="alert alert-danger" role="alert">
              {cancellationError}
            </div>
          )}
          {bookingsLoading ? (
            <p>Loading your bookings...</p>
          ) : bookings.length === 0 ? (
            <p className="text-muted">You don't have any bookings yet. Start by selecting a service below.</p>
          ) : (
            <div className="table-responsive">
              <table className="table table-sm table-hover">
                <thead className="table-light">
                  <tr>
                    <th>Service</th>
                    <th>Consultant</th>
                    <th>Date & Time</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {bookings.map(b => {
                    const startDate = new Date(b.start_time);
                    const dateTimeStr = startDate.toLocaleString();
                    return (
                      <tr key={b.booking_id}>
                        <td>{b.service_name}</td>
                        <td>{b.consultant_name}</td>
                        <td>{dateTimeStr}</td>
                        <td>
                          <span className={`badge ${b.state === 'CONFIRMED' ? 'bg-success' : b.state === 'REJECTED' ? 'bg-danger' : b.state === 'CANCELLED' ? 'bg-secondary' : 'bg-warning'}`}>
                            {b.state}
                          </span>
                        </td>
                        <td>
                          {b.state !== 'CANCELLED' && b.state !== 'REJECTED' && (
                            <button 
                              onClick={() => handleCancel(b.booking_id)}
                              className="btn btn-sm btn-danger"
                            >
                              Cancel
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {services.length === 0 ? (
        <div className="alert alert-info">
          <p>No services are currently available. Please check back later.</p>
        </div>
      ) : (
        <>
          <div className="card mb-4">
            <div className="card-body">
              <h5 className="card-title">Available Services</h5>
              <div className="d-grid gap-2">
                {services.map(s => (
                  <button 
                    key={s.service_id} 
                    onClick={() => selectService(s)}
                    className={`btn ${selectedService?.service_id === s.service_id ? 'btn-primary' : 'btn-outline-primary'}`}
                  >
                    <strong>{s.name || s.serviceName}</strong> - {s.duration} mins - ${s.price}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {bookingError && (
            <div className="alert alert-danger" role="alert">
              {bookingError}
            </div>
          )}

          {selectedService && (
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">
                  Available Times for {selectedService.name || selectedService.serviceName}
                </h5>
                
                {slotsLoading ? (
                  <p>Loading available time slots...</p>
                ) : slots.length === 0 ? (
                  <p className="text-muted">No available time slots for this service.</p>
                ) : (
                  <div className="row">
                    {slots.map(slot => {
                      const startDate = new Date(slot.start_time);
                      const endDate = new Date(slot.end_time);
                      const dateStr = startDate.toLocaleDateString();
                      const startTimeStr = startDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                      const endTimeStr = endDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                      
                      return (
                        <div key={slot.slot_id} className="col-md-6 mb-3">
                          <div className="card h-100">
                            <div className="card-body text-center">
                              <h6 className="card-title">{dateStr}</h6>
                              <p className="card-text">
                                <strong>{startTimeStr}</strong> - <strong>{endTimeStr}</strong>
                              </p>
                              <button 
                                onClick={() => handleBooking(slot)}
                                className="btn btn-success w-100"
                              >
                                Book This Time
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

export default ClientDashboard;
