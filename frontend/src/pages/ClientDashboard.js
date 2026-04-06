import { useEffect, useState } from "react";
import { getServices, getTimeslots, bookService } from "../services/api";
import "./Client.css";

function ClientDashboard() {
  const [services, setServices] = useState([]);
  const [slots, setSlots] = useState([]);
  const [selectedService, setSelectedService] = useState(null);
  const [loading, setLoading] = useState(true);

  const clientId = localStorage.getItem("client_id");

  useEffect(() => {
    async function fetchServices() {
      try {
        const data = await getServices();
        setServices(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    fetchServices();
  }, []);

  async function selectService(service) {
    setSelectedService(service);
    const s = await getTimeslots(service.consultant_id);
    setSlots(s);
  }

  async function handleBooking(slot) {
    await bookService({
      client_id: clientId,
      consultant_id: selectedService.consultant_id,
      service_id: selectedService.service_id,
      slot_id: slot.slot_id
    });

    alert("Booking successful!");
  }

  if (loading) {
    return <div className="text-center mt-5">Loading services...</div>;
  }

  return (
    <div className="full-page">
      <div className="login-box">
        <h2>Available Services</h2>

        {services.map(s => (
          <button key={s.service_id} onClick={() => selectService(s)}>
            {s.name || s.serviceName} - ${s.price}
          </button>
        ))}

        {slots.length > 0 && <h3>Available Slots</h3>}

        {slots.map(slot => (
          <button key={slot.slot_id} onClick={() => handleBooking(slot)}>
            {slot.start_time} - {slot.end_time}
          </button>
        ))}
      </div>
    </div>
  );
}

export default ClientDashboard;
