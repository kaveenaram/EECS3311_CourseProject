import { useEffect, useState } from "react";
import { getServices } from "../services/clientApi";

export default function BrowseServicesPage() {
  const [services, setServices] = useState([]);

  useEffect(() => {
    getServices().then(setServices);
  }, []);



  return (
    <div style={{ padding: "20px" }}>
      <h2>Services</h2>

      {services.map((s) => (
        <div key={s.id}>
          <p>{s.name}</p>
          <button>Book</button>
        </div>
      ))}
    </div>
  );
  
}