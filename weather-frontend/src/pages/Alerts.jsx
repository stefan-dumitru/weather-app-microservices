import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import alertApi from "../api/alertApi";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [form, setForm] = useState({
    city_name: "",
    latitude: "",
    longitude: "",
    condition: "temperature_below",
    threshold: "",
  });

  useEffect(() => {
    loadAlerts();
  }, []);

  async function loadAlerts() {
    const res = await alertApi.getAlerts();
    setAlerts(res);
  }

  async function handleAdd(e) {
    e.preventDefault();
    await alertApi.createAlert({
      city_name: form.city_name,
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
      condition: form.condition,
      threshold: parseFloat(form.threshold),
    });
    loadAlerts();
  }

  return (
    <>
      <Navbar />

      <div style={{ padding: 20 }}>
        <h2>Weather Alerts</h2>

        <form onSubmit={handleAdd} style={{ marginBottom: 20 }}>
          <input
            type="text"
            placeholder="City Name"
            onChange={e => setForm({ ...form, city_name: e.target.value })}
          />
          <input
            type="number"
            placeholder="Latitude"
            onChange={e => setForm({ ...form, latitude: e.target.value })}
          />
          <input
            type="number"
            placeholder="Longitude"
            onChange={e => setForm({ ...form, longitude: e.target.value })}
          />

          <select onChange={e => setForm({ ...form, condition: e.target.value })}>
            <option value="temperature_below">Temperature Below</option>
            <option value="temperature_above">Temperature Above</option>
            <option value="humidity_above">Humidity Above</option>
          </select>

          <input
            type="number"
            placeholder="Threshold"
            onChange={e => setForm({ ...form, threshold: e.target.value })}
          />

          <button type="submit">Add Alert</button>
        </form>

        <ul>
          {alerts.map(a => (
            <li key={a.id}>
              {a.city_name} — {a.condition} {a.threshold}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}