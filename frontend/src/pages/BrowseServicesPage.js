import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getServices } from "../services/api";

export default function BrowseServicesPage() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchServices() {
      try {
        setError(null);
        const data = await getServices();
        
        if (!data || !Array.isArray(data) || data.length === 0) {
          setError("No services are currently available. Please try again later.");
          setServices([]);
        } else {
          setServices(data);
        }
        setLoading(false);
      } catch (err) {
        console.error("Error fetching services:", err);
        setError("Failed to load services. Please refresh the page or try again later.");
        setLoading(false);
      }
    }
    fetchServices();
  }, []);

  if (loading) {
    return (
      <div className="container mt-5 text-center">
        <p>Loading services...</p>
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
    <div style={{ padding: "20px" }}>
      <h2>Available Consulting Services</h2>

      <button onClick={() => navigate(-1)} className="btn btn-secondary mb-3">
        ← Back
      </button>

      {services.length === 0 ? (
        <div className="alert alert-info">
          <p>No services are currently available. Please check back later.</p>
        </div>
      ) : (
        <div className="row">
          {services.map((s) => (
            <div key={s.service_id} className="col-md-6 mb-4">
              <div className="card h-100">
                <div className="card-body">
                  <h5 className="card-title">{s.name || s.serviceName}</h5>
                  {s.description && <p className="card-text">{s.description}</p>}
                  <p className="card-text">
                    <strong>Duration:</strong> {s.duration} minutes<br />
                    <strong>Price:</strong> ${s.price?.toFixed(2) || "0.00"}
                  </p>
                  <button 
                    onClick={() => navigate("/client-dashboard")}
                    className="btn btn-primary"
                  >
                    Book Now
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
