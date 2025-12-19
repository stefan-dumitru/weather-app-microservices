import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import alertApi from "../api/alertApi";
import locationApi from "../api/locationApi";
import AddAlert from "./AddAlert";

export default function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [locations, setLocations] = useState([]);

  useEffect(() => {
    loadAlerts();
    loadLocations();
  }, []);

  async function loadAlerts() {
    const res = await alertApi.getAlerts();
    setAlerts(res.data);
  }

  async function loadLocations() {
    const res = await locationApi.getLocations();
    setLocations(res.data);
  }

  return (
    <>
      <Navbar />

      <div style={{ padding: 20 }}>
        <h2>Weather Alerts</h2>

        <AddAlert locations={locations} onAdded={loadAlerts} />

        <hr style={{ margin: "20px 0" }} />

        <ul>
          {alerts.map((a) => (
            <li key={a.id} style={{ marginBottom: 10 }}>
              <strong>{a.city_name}</strong> — {a.condition} {a.threshold} — Range: {a.day_range === 0 ? "Today" : `Next ${a.day_range} days`}

              <button
                onClick={async () => {
                  await alertApi.toggleAlert(a.id);
                  loadAlerts();
                }}
                style={{ marginLeft: 10 }}
              >
                {a.active ? "Deactivate" : "Activate"}
              </button>

              <button
                onClick={async () => {
                  if (confirm("Delete this alert?")) {
                    await alertApi.deleteAlert(a.id);
                    loadAlerts();
                  }
                }}
                style={{ marginLeft: 5, color: "red" }}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}