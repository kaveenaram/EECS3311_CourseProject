import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultantTimeslots, addTimeslot, deleteTimeslot } from "../services/api";

export default function ManageTimeslots() {
  const [timeslots, setTimeslots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const navigate = useNavigate();
  const consultantId = localStorage.getItem("consultant_id") || "consultant1";

  useEffect(() => {
    async function fetchTimeslots() {
      try {
        const data = await getConsultantTimeslots(consultantId);
        setTimeslots(Array.isArray(data) ? data : []);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setLoading(false);
      }
    }
    fetchTimeslots();
  }, [consultantId]);

  const handleAdd = async () => {
    if (!date || !startTime || !endTime) {
      alert("Please enter date, start time, and end time");
      return;
    }
    try {
      const newSlot = await addTimeslot(consultantId, { 
        start_time: startTime, 
        end_time: endTime,
        date: date
      });
      if (newSlot) {
        setTimeslots([...timeslots, newSlot]);
        setDate(new Date().toISOString().split('T')[0]);
        setStartTime("");
        setEndTime("");
        alert("Timeslot added successfully!");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to add timeslot");
    }
  };

  const handleDelete = async (slotId) => {
    try {
      await deleteTimeslot(consultantId, slotId);
      setTimeslots(timeslots.filter((s) => s.slot_id !== slotId));
      alert("Timeslot deleted successfully!");
    } catch (err) {
      console.error(err);
      alert("Failed to delete timeslot");
    }
  };

  if (loading) {
    return (
      <div className="container mt-4 text-center">
        <p>Loading timeslots...</p>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h2>Manage Timeslots</h2>
        <button className="btn btn-secondary" onClick={() => navigate("/consultant-dashboard")}>
          Back
        </button>
      </div>

      {timeslots.length === 0 && (
        <div className="alert alert-info text-center mb-4">
          <p>You don't have any timeslots yet. Create your first one below!</p>
        </div>
      )}

      <div className="card mb-4">
        <div className="card-body">
          <h5 className="card-title">Add New Timeslot</h5>
          <div className="form-group mb-3">
            <label>Date:</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              className="form-control"
              min={new Date().toISOString().split('T')[0]}
            />
          </div>
          <div className="row mb-3">
            <div className="col-md-6">
              <label>Start Time:</label>
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="form-control"
              />
            </div>
            <div className="col-md-6">
              <label>End Time:</label>
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                className="form-control"
              />
            </div>
          </div>
          <button className="btn btn-success" onClick={handleAdd}>
            Add Timeslot
          </button>
        </div>
      </div>

      {timeslots.length > 0 && (
        <div className="table-responsive">
          <table className="table table-bordered table-hover">
            <thead className="table-dark">
              <tr>
                <th>Slot ID</th>
                <th>Date</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Available</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {timeslots.map((s) => {
                const startDate = new Date(s.start_time);
                const endDate = new Date(s.end_time);
                return (
                  <tr key={s.slot_id}>
                    <td>{s.slot_id}</td>
                    <td>{startDate.toLocaleDateString()}</td>
                    <td>{startDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
                    <td>{endDate.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</td>
                    <td>{s.available ? "Yes" : "No"}</td>
                    <td>
                      <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.slot_id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}