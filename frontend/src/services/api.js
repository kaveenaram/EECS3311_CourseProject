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
________________________________________
