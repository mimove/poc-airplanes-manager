import { useEffect, useState } from "react";
import { api } from "../api/client";
import AlertBadge from "../components/AlertBadge";

const EMPTY = {
  plate_number: "",
  type: "",
  last_maintenance_date: "",
  next_maintenance_date: "",
  capacity: "",
  owner_id: "",
  owner_name: "",
  hangar_id: "",
  fuel_capacity: "",
};

export default function AirplanesPage() {
  const [airplanes, setAirplanes] = useState([]);
  const [form, setForm] = useState(EMPTY);
  const [error, setError] = useState(null);

  const load = async () => {
    try {
      setAirplanes(await api.airplanes.list());
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
      await api.airplanes.create({
        ...form,
        capacity: parseInt(form.capacity, 10),
        fuel_capacity: parseInt(form.fuel_capacity, 10),
      });
      setForm(EMPTY);
      await load();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h2>Airplanes</h2>
      <form onSubmit={handleSubmit}>
        <input required placeholder="Plate (e.g. EC-XYZ1)" value={form.plate_number} onChange={set("plate_number")} />
        <input required placeholder="Type (e.g. Cessna 208)" value={form.type} onChange={set("type")} />
        <input required type="date" title="Last maintenance date" value={form.last_maintenance_date} onChange={set("last_maintenance_date")} />
        <input required type="date" title="Next maintenance date" value={form.next_maintenance_date} onChange={set("next_maintenance_date")} />
        <input required type="number" placeholder="Capacity (seats)" value={form.capacity} onChange={set("capacity")} />
        <input required placeholder="Owner ID" value={form.owner_id} onChange={set("owner_id")} />
        <input required placeholder="Owner name" value={form.owner_name} onChange={set("owner_name")} />
        <input required placeholder="Hangar ID" value={form.hangar_id} onChange={set("hangar_id")} />
        <input required type="number" placeholder="Fuel capacity (L)" value={form.fuel_capacity} onChange={set("fuel_capacity")} />
        <button type="submit">Add Airplane</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>
            <th>Plate</th>
            <th>Type</th>
            <th>Capacity</th>
            <th>Hangar</th>
            <th>Next Maintenance</th>
            <th>Days Left</th>
            <th>Alerts</th>
          </tr>
        </thead>
        <tbody>
          {airplanes.map((a) => (
            <tr key={a.plate_number}>
              <td>{a.plate_number}</td>
              <td>{a.type}</td>
              <td>{a.capacity}</td>
              <td>{a.hangar_id}</td>
              <td>{a.next_maintenance_date}</td>
              <td>{a.days_until_maintenance}</td>
              <td>
                <AlertBadge active={a.maintenance_alert} label="Maintenance" />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
