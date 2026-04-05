import { useEffect, useState } from "react";
import { getServices } from "../services/clientApi";

export default function BrowseServicesPage() {
  const [services, setServices] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getServices().then(setServices);
  }, []);

  function handleBooking(serviceName) {
    setMessage(`Successfully booked: ${serviceName}`);
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Services</h2>

      {services.map((s) => (
        <div key={s.id} style={{ marginBottom: "10px" }}>
          <p>{s.name}</p>

          <button onClick={() => handleBooking(s.name)}>
            Book
          </button>
        </div>
      ))}

      {message && <p style={{ color: "green" }}>{message}</p>}
    </div>

  );
}
