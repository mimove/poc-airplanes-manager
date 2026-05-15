const BASE = "/api";

async function request(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: body !== undefined ? { "Content-Type": "application/json" } : {},
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export const api = {
  hangars: {
    list: () => request("GET", "/hangars/"),
    create: (data) => request("POST", "/hangars/", data),
  },
  airplanes: {
    list: () => request("GET", "/airplanes/"),
    create: (data) => request("POST", "/airplanes/", data),
  },
  flights: {
    list: () => request("GET", "/flights/"),
    create: (data) => request("POST", "/flights/", data),
  },
  passengers: {
    list: () => request("GET", "/passengers/"),
    create: (data) => request("POST", "/passengers/", data),
  },
};
