import { useEffect, useState } from "react";
import { api } from "../api/client";
import AlertBadge from "../components/AlertBadge";

const EMPTY_FORM = {
  flight_id: "",
  plate_number: "",
  origin: "",
  destination: "",
  departure_time: "",
  arrival_time: "",
  occupied_seats: "",
  fuel_consumption: "",
  passengers: [],
};

const EMPTY_ENTRY = { passenger_id: "", status: "BOARDING" };

export default function FlightsPage() {
  const [flights, setFlights] = useState([]);
  const [allPassengers, setAllPassengers] = useState([]);
  const [allAirplanes, setAllAirplanes] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [entry, setEntry] = useState(EMPTY_ENTRY);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      const [fl, ps, ap] = await Promise.all([
        api.flights.list(),
        api.passengers.list(),
        api.airplanes.list(),
      ]);
      setFlights(fl);
      setAllPassengers(ps);
      setAllAirplanes(ap);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, []);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));
  const setEntry_ = (field) => (e) => setEntry((en) => ({ ...en, [field]: e.target.value }));

  const addPassenger = () => {
    if (!entry.passenger_id) return;
    setForm((f) => ({ ...f, passengers: [...f.passengers, { ...entry }] }));
    setEntry(EMPTY_ENTRY);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await api.flights.create({
        ...form,
        occupied_seats: parseInt(form.occupied_seats, 10),
        fuel_consumption: parseInt(form.fuel_consumption, 10),
        departure_time: form.departure_time + ":00Z",
        arrival_time: form.arrival_time + ":00Z",
      });
      setForm(EMPTY_FORM);
      setEntry(EMPTY_ENTRY);
      await load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Flights</h2>
      <form onSubmit={handleSubmit}>
        <input required placeholder="Flight ID (e.g. FL-001)" value={form.flight_id} onChange={set("flight_id")} />

        <select required value={form.plate_number} onChange={set("plate_number")}
          style={{ minWidth: 180 }}>
          <option value="">Select airplane</option>
          {allAirplanes.map((a) => (
            <option key={a.plate_number} value={a.plate_number}>
              {a.plate_number} ({a.type})
            </option>
          ))}
        </select>

        <input required placeholder="Origin" value={form.origin} onChange={set("origin")} />
        <input required placeholder="Destination" value={form.destination} onChange={set("destination")} />

        <input required type="datetime-local" title="Departure time" value={form.departure_time} onChange={set("departure_time")} />
        <input required type="datetime-local" title="Arrival time" value={form.arrival_time} onChange={set("arrival_time")} />

        <input required type="number" placeholder="Occupied seats" value={form.occupied_seats} onChange={set("occupied_seats")} />
        <input required type="number" placeholder="Fuel consumed (L)" value={form.fuel_consumption} onChange={set("fuel_consumption")} />

        <div className="passenger-entry">
          <strong>Add passenger:</strong>
          <select value={entry.passenger_id} onChange={setEntry_("passenger_id")} style={{ minWidth: 160 }}>
            <option value="">— select —</option>
            {allPassengers.map((p) => (
              <option key={p.passenger_id} value={p.passenger_id}>
                {p.name} ({p.passenger_id})
              </option>
            ))}
          </select>
          <select value={entry.status} onChange={setEntry_("status")}>
            <option value="BOARDING">BOARDING</option>
            <option value="BOARDED">BOARDED</option>
            <option value="NO_SHOW">NO_SHOW</option>
          </select>
          <button type="button" onClick={addPassenger}>Add</button>
          {form.passengers.length > 0 && (
            <ul className="passenger-list">
              {form.passengers.map((fp, i) => (
                <li key={i}>{fp.passenger_id} — {fp.status}</li>
              ))}
            </ul>
          )}
        </div>

        <button type="submit">Create Flight</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Airplane</th>
            <th>Origin → Destination</th>
            <th>Departure</th>
            <th>Empty Seats</th>
            <th>Passengers</th>
            <th>Alerts</th>
          </tr>
        </thead>
        <tbody>
          {flights.map((f) => (
            <tr key={f.flight_id}>
              <td>{f.flight_id}</td>
              <td>{f.plate_number}</td>
              <td>{f.origin} → {f.destination}</td>
              <td>{new Date(f.departure_time).toLocaleString()}</td>
              <td>{f.empty_seats}</td>
              <td>{f.passengers.length}</td>
              <td>
                <AlertBadge active={f.empty_seats_alert} label="Empty seats" />
                <AlertBadge active={f.fuel_alert} label="Fuel" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
