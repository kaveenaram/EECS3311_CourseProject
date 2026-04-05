export default function AdminDashboard() {

  async function approveConsultant() {
    await fetch("http://localhost:5000/api/admin/approve/consultant1", {
      method: "POST"
    });
    alert("Consultant approved!");
  }

  return (
    <div>
      <h1>Admin Dashboard</h1>

      <button onClick={approveConsultant}>
        Approve Consultant1
      </button>
    </div>
  );
}