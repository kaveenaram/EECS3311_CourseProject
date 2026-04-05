import { useEffect, useState } from "react";
import { getPayments } from "../services/clientApi";


export default function PaymentPage() {
  const [payments, setPayments] = useState([]);

  useEffect(() => {
    getPayments().then(setPayments);
  }, []);



  return (
    <div style={{ padding: "20px" }}>
      <h2>Payments</h2>

      {payments.map((p) => (
        <div key={p.id}>
          <p>{p.amount} - {p.status}</p>
        </div>
      ))}
    </div>
  );

}