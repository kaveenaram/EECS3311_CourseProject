const BASE_URL = "http://localhost:5000"; 

export async function getData(endpoint) {
    const res = await fetch(`${BASE_URL}/${endpoint}`);
    return res.json();
}

export async function postData(endpoint, data) {
    const res = await fetch(`${BASE_URL}/${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
}

// Consultant login
export async function loginConsultant(userId, password) {
  try {
    const res = await postData("api/consultant/login", { user_id: userId, password });
    //console.log("Raw login response:", res); // <--- used for testing 
    if (res.success) {
      return { 
        success: true, 
        consultant: { id: res.consultant_id, name: res.name } 
      };
    } else {
      return { success: false, consultant: null };
    }
  } catch (err) {
    console.error("Login error:", err);
    return { success: false, consultant: null };
  }
}

// Get consultant bookings with fallback to mock data
export async function getConsultantBookings(consultantId) {
  try {
    // Try fetching from backend
    const res = await getData(`api/consultant/${consultantId}/bookings`);
    // If backend returns bookings, use them
    return res.bookings || [];
  } catch (err) {
    console.error("Backend unavailable, using mock data:", err);

    // Mock bookings fallback
    const mockBookings = [
      {
        booking_id: "b1",
        client_name: "John Doe",
        service_name: "Career Coaching",
        start_time: "2026-04-05T09:00:00",
        end_time: "2026-04-05T10:00:00",
        state: "PENDING"
      },
      {
        booking_id: "b2",
        client_name: "Jane Smith",
        service_name: "Resume Review",
        start_time: "2026-04-05T10:30:00",
        end_time: "2026-04-05T11:00:00",
        state: "CONFIRMED"
      },
      {
        booking_id: "b3",
        client_name: "Mark Taylor",
        service_name: "Interview Prep",
        start_time: "2026-04-05T11:30:00",
        end_time: "2026-04-05T12:00:00",
        state: "REJECTED"
      }
    ];

    // Simulate async network call
    return new Promise((resolve) => setTimeout(() => resolve(mockBookings), 500));
  }
}

export async function getConsultantTimeslots(consultantId) {
  // fetch timeslots from backend or return mock
  return [
    { slot_id: "ts1", start_time: "09:00", end_time: "10:00", available: true },
    { slot_id: "ts2", start_time: "10:30", end_time: "11:30", available: true },
  ];
}

export async function addTimeslot(consultantId, { start_time, end_time }) {
  // send POST request to backend, here just mock
  const newSlot = { slot_id: `ts${Date.now()}`, start_time, end_time, available: true };
  return newSlot;
}

export async function deleteTimeslot(consultantId, slotId) {
  // send DELETE request to backend
  return true;
}

// Fetch consultant services
export async function getConsultantServices(consultantId) {
  return [
    { service_id: "s1", serviceName: "Career Coaching", duration: 60, price: 120 },
    { service_id: "s2", serviceName: "Resume Review", duration: 30, price: 60 },
  ];
}

export async function addService(consultantId, { serviceName, duration, price }) {
  const newService = {
    service_id: `s${Date.now()}`,
    serviceName,
    duration,
    price,
  };
  return newService;
}

export async function deleteService(consultantId, serviceId) {
  return true;
}

export async function confirmBooking(bookingId) {
  return await postData(`api/bookings/${bookingId}/confirm`);
}

export async function rejectBooking(bookingId) {
  return await postData(`api/bookings/${bookingId}/reject`);
}