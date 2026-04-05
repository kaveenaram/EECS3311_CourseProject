import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultantServices, addService, deleteService } from "../services/api";

export default function ManageServices() {
  const [services, setServices] = useState([]);
  const [name, setName] = useState("");
  const [duration, setDuration] = useState("");
  const [price, setPrice] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    async function fetchServices() {
      const data = await getConsultantServices("consultant1");
      setServices(data);
    }
    fetchServices();
  }, []);

  const handleAdd = async () => {
    if (!name || !duration || !price) return;
    const newService = await addService("consultant1", {
      serviceName: name,
      duration: parseInt(duration),
      price: parseFloat(price),
    });
    setServices([...services, newService]);
    setName("");
    setDuration("");
    setPrice("");
  };

  const handleDelete = async (serviceId) => {
    await deleteService("consultant1", serviceId);
    setServices(services.filter((s) => s.service_id !== serviceId));
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Manage Services</h2>

      {/* Add Service Form */}
      <div className="mb-3 d-flex justify-content-center gap-2">
        <input
          type="text"
          placeholder="Service Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="form-control w-auto"
        />
        <input
          type="number"
          placeholder="Duration (mins)"
          value={duration}
          onChange={(e) => setDuration(e.target.value)}
          className="form-control w-auto"
        />
        <input
          type="number"
          placeholder="Price"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          className="form-control w-auto"
        />
        <button className="btn btn-success" onClick={handleAdd}>
          Add Service
        </button>
        <button className="btn btn-secondary" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>

      {/* Services Table */}
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
              <td>{s.serviceName}</td>
              <td>{s.duration} mins</td>
              <td>${s.price}</td>
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
  );
}