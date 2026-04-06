import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getServices } from "../services/api";

export default function BrowseServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

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

  if (loading) {
    return <div className="text-center mt-5">Loading services...</div>;
  }

  return (
    <div style={{ padding: "20px" }}>
      <h2>Available Services</h2>

      <button onClick={() => navigate(-1)} className="btn btn-secondary mb-3">
        Back
      </button>

      {services.length === 0 ? (
        <p>No services available</p>
      ) : (
        services.map((s) => (
          <div key={s.service_id} style={{ marginBottom: "10px", padding: "10px", border: "1px solid #ccc" }}>
            <p><strong>{s.name || s.serviceName}</strong></p>
            <p>Price: ${s.price}</p>
            <p>Consultant ID: {s.consultant_id}</p>
            <button 
              onClick={() => navigate("/client-dashboard")}
              className="btn btn-primary btn-sm"
            >
              View & Book
            </button>
          </div>
        ))
      )}
    </div>
  );
}
