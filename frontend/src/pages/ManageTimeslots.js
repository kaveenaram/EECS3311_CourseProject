import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { getConsultantTimeslots, addTimeslot, deleteTimeslot } from "../services/api";

export default function ManageTimeslots() {
  const [timeslots, setTimeslots] = useState([]);
  const [startTime, setStartTime] = useState("");
  const [endTime, setEndTime] = useState("");
  const navigate = useNavigate();
  const consultantId = localStorage.getItem("consultant_id") || "consultant1";

  useEffect(() => {
    async function fetchTimeslots() {
      const data = await getConsultantTimeslots(consultantId);
      setTimeslots(data);
    }
    fetchTimeslots();
  }, [consultantId]);

  const handleAdd = async () => {
    if (!startTime || !endTime) return;
    const newSlot = await addTimeslot(consultantId, { start_time: startTime, end_time: endTime });
    setTimeslots([...timeslots, newSlot]);
    setStartTime("");
    setEndTime("");
  };

  const handleDelete = async (slotId) => {
    await deleteTimeslot(consultantId, slotId);
    setTimeslots(timeslots.filter((s) => s.slot_id !== slotId));
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center mb-4">Manage Timeslots</h2>

      <div className="mb-3 d-flex justify-content-center gap-2">
        <input
          type="time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          className="form-control w-auto"
        />
        <input
          type="time"
          value={endTime}
          onChange={(e) => setEndTime(e.target.value)}
          className="form-control w-auto"
        />
        <button className="btn btn-success" onClick={handleAdd}>
          Add Timeslot
        </button>
        <button className="btn btn-secondary" onClick={() => navigate(-1)}>
          Back
        </button>
      </div>

      <table className="table table-bordered table-hover">
        <thead className="table-dark">
          <tr>
            <th>Slot ID</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Available</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {timeslots.map((s) => (
            <tr key={s.slot_id}>
              <td>{s.slot_id}</td>
              <td>{s.start_time}</td>
              <td>{s.end_time}</td>
              <td>{s.available ? "Yes" : "No"}</td>
              <td>
                <button className="btn btn-danger btn-sm" onClick={() => handleDelete(s.slot_id)}>
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