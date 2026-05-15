import { useEffect, useState } from "react";
import { api } from "../api/client";

const EMPTY = { passenger_id: "", name: "", national_id: "", date_of_birth: "" };

export default function PassengersPage() {
  const [passengers, setPassengers] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      setPassengers(await api.passengers.list());
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => { load(); }, []);

  const set = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    try {
      await api.passengers.create(form);
      setForm(EMPTY);
      await load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Passengers</h2>
      <form onSubmit={handleSubmit}>
        <input required placeholder="ID (e.g. P-001)" value={form.passenger_id} onChange={set("passenger_id")} />
        <input required placeholder="Full name" value={form.name} onChange={set("name")} />
        <input required placeholder="National ID" value={form.national_id} onChange={set("national_id")} />
        <input required type="date" title="Date of birth" value={form.date_of_birth} onChange={set("date_of_birth")} />
        <button type="submit">Add Passenger</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>National ID</th>
            <th>Date of Birth</th>
          </tr>
        </thead>
        <tbody>
          {passengers.map((p) => (
            <tr key={p.passenger_id}>
              <td>{p.passenger_id}</td>
              <td>{p.name}</td>
              <td>{p.national_id}</td>
              <td>{p.date_of_birth}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
