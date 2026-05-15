import { useEffect, useState } from "react";
import { api } from "../api/client";

const EMPTY = { id: "", name: "", location: "" };

export default function HangarsPage() {
  const [hangars, setHangars] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      setHangars(await api.hangars.list());
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
      await api.hangars.create(form);
      setForm(EMPTY);
      await load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Hangars</h2>
      <form onSubmit={handleSubmit}>
        <input required placeholder="ID (e.g. H-01)" value={form.id} onChange={set("id")} />
        <input required placeholder="Name" value={form.name} onChange={set("name")} />
        <input placeholder="Location" value={form.location} onChange={set("location")} />
        <button type="submit">Add Hangar</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
          </tr>
        </thead>
        <tbody>
          {hangars.map((h) => (
            <tr key={h.id}>
              <td>{h.id}</td>
              <td>{h.name}</td>
              <td>{h.location ?? "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
