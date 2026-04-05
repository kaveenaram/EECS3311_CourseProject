export async function getServices() {
  return [
    { id: 1, name: "Career Consulting" },
    { id: 2, name: "Business Strategy" }
  ];
}

export async function getBookings() {
  return [
    { id: 1, service: "Career Consulting", status: "Confirmed" }
  ];
}

export async function getPayments() {
  return [
    { id: 1, amount: "$100", status: "Paid" }
  ];
}