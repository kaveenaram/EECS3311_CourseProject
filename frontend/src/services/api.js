const BASE_URL = process.env.REACT_APP_API_URL || "http://backend:5000";

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

// Get consultant bookings 
export async function getConsultantBookings(consultantId) {
  try {
    const res = await getData(`api/consultant/${consultantId}/bookings`);
    console.log("Backend response:", res);

    return res || [];
  } catch (err) {
    console.error("Error fetching bookings:", err);
    return []; // just fail safely, NO mock data
  }
}

export async function getConsultantTimeslots(consultantId) {
  return await getData(`api/consultant/${consultantId}/timeslots`);
}

export async function addTimeslot(consultantId, { start_time, end_time }) {
  return await postData(`api/consultant/${consultantId}/timeslots`, {
    start_time,
    end_time
  });
}

export async function deleteTimeslot(consultantId, slotId) {
  return await postData(`api/consultant/${consultantId}/timeslots/${slotId}/delete`);
}

// Fetch consultant services
export async function getConsultantServices(consultantId) {
  return await getData(`api/consultant/${consultantId}/services`);
}

export async function addService(consultantId, { serviceName, duration, price }) {
  return await postData(`api/consultant/${consultantId}/services`, {
    serviceName,
    duration,
    price
  });
}

export async function deleteService(consultantId, serviceId) {
  return await postData(`api/consultant/${consultantId}/services/${serviceId}/delete`);
}

export async function confirmBooking(bookingId) {
  return await postData(`api/bookings/${bookingId}/confirm`);
}

export async function rejectBooking(bookingId) {
  return await postData(`api/bookings/${bookingId}/reject`);
}