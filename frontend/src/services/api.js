const BASE_URL = "http://localhost:3000"; 

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

export async function putData(endpoint, data) {
    const res = await fetch(`${BASE_URL}/${endpoint}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
}

// Consultant login
export async function loginConsultant(username, password) {
  try {
    const res = await postData("api/consultant/login", { username, password });
    // return both success status and consultant data
    return { success: res.success, consultant: res.consultant || null };
  } catch (err) {
    console.error(err);
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