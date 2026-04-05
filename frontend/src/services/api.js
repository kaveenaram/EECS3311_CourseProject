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

// Get consultant bookings
export async function getConsultantBookings(consultantId) {
  try {
    const res = await getData(`api/consultant/${consultantId}/bookings`);
    return res.bookings || [];
  } catch (err) {
    console.error(err);
    return [];
  }
}