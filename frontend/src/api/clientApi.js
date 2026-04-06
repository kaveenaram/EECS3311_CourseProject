const BASE_URL = "http://localhost:5000";

// Login
export async function clientLogin(data) {
  const res = await fetch(`${BASE_URL}/api/client/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

// Signup
export async function clientSignup(data) {
  const res = await fetch(`${BASE_URL}/api/client/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}

// Services
export async function getServices() {
  const res = await fetch(`${BASE_URL}/api/services`);
  return res.json();
}

// Timeslots
export async function getTimeslots(consultantId) {
  const res = await fetch(`${BASE_URL}/api/timeslots/${consultantId}`);
  return res.json();
}

// Booking
export async function bookService(data) {
  const res = await fetch(`${BASE_URL}/api/book`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  return res.json();
}