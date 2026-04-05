import { useEffect, useState } from "react";
import { getConsultantBookings } from "../services/api";
import BookingTable from "../components/BookingTable";

export default function ConsultantDashboard() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    async function fetchBookings() {
      const data = await getConsultantBookings("consultant1"); // temporary hardcoded
      setBookings(data);
    }
    fetchBookings();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Consultant Dashboard</h1>
      <BookingTable bookings={bookings} />
    </div>
  );
}
