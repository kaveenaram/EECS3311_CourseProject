export default function BookingTable({ bookings }) {
  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px" }}>
      <thead>
        <tr>
          <th style={{ border: "1px solid black", padding: "8px" }}>Booking ID</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Client</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Service</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>Time</th>
          <th style={{ border: "1px solid black", padding: "8px" }}>State</th>
        </tr>
      </thead>
      <tbody>
        {bookings.map((b) => (
          <tr key={b.booking_id}>
            <td style={{ border: "1px solid black", padding: "8px" }}>{b.booking_id}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{b.client_name}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{b.service_name}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{b.time}</td>
            <td style={{ border: "1px solid black", padding: "8px" }}>{b.state}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
