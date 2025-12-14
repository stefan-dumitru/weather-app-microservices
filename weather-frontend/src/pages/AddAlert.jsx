import { useState } from "react";
import alertApi from "../api/alertApi";

export default function AddAlert({ locations }) {
  const [locationId, setLocationId] = useState("");
  const [condition, setCondition] = useState("temp_above");
  const [threshold, setThreshold] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();

    const loc = locations.find(l => l.id === Number(locationId));
    if (!loc) return alert("Please select a location");

    try {
      await alertApi.addAlert({
        city_name: loc.name,
        latitude: loc.latitude,
        longitude: loc.longitude,
        condition,
        threshold: threshold ? Number(threshold) : 0,
      });

      alert("✅ Alert created!");
      setThreshold("");
    } catch (err) {
      console.error(err);
      alert("❌ Failed to create alert");
    }
  }

  return (
    <div className="card" style={{ marginBottom: 20 }}>
      <h3>Add Weather Alert</h3>

      <form onSubmit={handleSubmit}>
        {/* LOCATION */}
        <select
          value={locationId}
          onChange={(e) => setLocationId(e.target.value)}
          required
        >
          <option value="">Select location</option>
          {locations.map((loc) => (
            <option key={loc.id} value={loc.id}>
              {loc.name}
            </option>
          ))}
        </select>

        {/* CONDITION */}
        <select
          value={condition}
          onChange={(e) => setCondition(e.target.value)}
        >
          <option value="temp_above">Temperature above</option>
          <option value="temp_below">Temperature below</option>
          <option value="wind_above">Wind above</option>
          <option value="wind_below">Wind below</option>
          <option value="rain">Rain</option>
          <option value="snow">Snow</option>
        </select>

        {/* THRESHOLD */}
        {condition.includes("temp") || condition.includes("wind") ? (
          <input
            type="number"
            placeholder="Threshold"
            value={threshold}
            onChange={(e) => setThreshold(e.target.value)}
            required
          />
        ) : null}

        <button type="submit">Create Alert</button>
      </form>
    </div>
  );
}