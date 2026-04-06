import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultantServices, addService, deleteService } from "../services/api";

export default function ManageServices() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");
  const [price, setPrice] = useState("");
  const navigate = useNavigate();
  const consultantId = localStorage.getItem("consultant_id") || "consultant1";

  useEffect(() => {
    async function fetchServices() {
      try {
        const data = await getConsultantServices(consultantId);
        setServices(Array.isArray(data) ? data : []);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    fetchServices();
  }, [consultantId]);

  const handleAdd = async () => {
    if (!name || !duration || !price) {
      alert("Please fill in all fields");
      return;
    }
    try {
      const newService = await addService(consultantId, {
        serviceName: name,
        duration: parseInt(duration),
        price: parseFloat(price),
      });
      if (newService) {
        setServices([...services, newService]);
        setName("");
        setDuration("");
        setPrice("");
        alert("Service added successfully!");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to add service");
    }
  };

  const handleDelete = async (serviceId) => {
    try {
      await deleteService(consultantId, serviceId);
      setServices(services.filter((s) => s.service_id !== serviceId));
      alert("Service deleted successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to delete service");
    }
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <p>Loading services...</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Manage Services</h2>

      {services.length === 0 && (
        <div className="alert alert-info text-center mb-4">
          <p>You don't have any services yet. Create your first one below!</p>
        </div>
      )}

      {/* Add Service Form */}
      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Add New Service</h5>
          <div className="d-flex gap-2 align-items-end">
            <div className="form-group">
              <label>Service Name:</label>
              <input
                type="text"
                placeholder="e.g., Career Coaching"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="form-control"
              />
            </div>
            <div className="form-group">
              <label>Duration (minutes):</label>
              <input
                type="number"
                placeholder="60"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                className="form-control"
              />
            </div>
            <div className="form-group">
              <label>Price ($):</label>
              <input
                type="number"
                placeholder="100.00"
                step="0.01"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                className="form-control"
              />
            </div>
            <button className="btn btn-success" onClick={handleAdd}>
              Add Service
            </button>
            <button className="btn btn-secondary" onClick={() => navigate(-1)}>
              Back
            </button>
          </div>
        </div>
      </div>

      {/* Services Table */}
      {services.length > 0 && (
        <div className="table-responsive">
          <table className="table table-bordered table-hover">
            <thead className="table-dark">
              <tr>
                <th>Service ID</th>
                <th>Name</th>
                <th>Duration</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {services.map((s) => (
                <tr key={s.service_id}>
                  <td>{s.service_id}</td>
                  <td>{s.name || s.serviceName}</td>
                  <td>{s.duration} mins</td>
                  <td>${s.price?.toFixed(2)}</td>
                  <td>
                    <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.service_id)}>
                      Delete
                    </button>
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