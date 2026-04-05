import { useEffect, useState } from "react";
import { getBookings } from "../services/clientApi";


export default function BookingHistoryPage() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    getBookings().then(setBookings);
  }, []);



  return (
    <div style={{ padding: "20px" }}>
      <h2>Booking History</h2>

      {bookings.map((b) => (
        <div key={b.id}>
          <p>{b.service} - {b.status}</p>
          <button>Cancel</button>
        </div>
      ))}
    </div>
  );

  
}