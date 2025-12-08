import { useEffect, useState } from "react";
import locationApi from "../api/locationApi";
import weatherApi from "../api/weatherApi";
import useNotifications from "../hooks/useNotifications";
import NotificationToast from "../components/NotificationToast";

export default function Dashboard() {
  const [locations, setLocations] = useState([]);
  const [weather, setWeather] = useState({});
  const [city, setCity] = useState("");
  const [notifications, setNotifications] = useState([]);

  const token = localStorage.getItem("access_token");

  useNotifications(token, (msg) => {
    setNotifications((prev) => [...prev, msg]);
  });

  async function load() {
    const locRes = await locationApi.getLocations();
    setLocations(locRes.data);

    const w = {};
    for (const loc of locRes.data) {
      const res = await weatherApi.getCurrent(loc.latitude, loc.longitude);
      w[loc.id] = res.data;
    }
    setWeather(w);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleAddLocation(e) {
    e.preventDefault();

    // Automatic Geocoding
    const geodata = await fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${city}`
    ).then(r => r.json());

    if (!geodata.length) {
      alert("City not found");
      return;
    }

    const lat = geodata[0].lat;
    const lon = geodata[0].lon;

    // Send to API Gateway
    await locationApi.addLocation({
      name: city,
      latitude: lat,
      longitude: lon,
    });

    setCity("");
    load(); // reload dashboard
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Your Weather Dashboard</h2>

      {/* FORM Add Location */}
      <form onSubmit={handleAddLocation} style={{ marginBottom: 20 }}>
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={e => setCity(e.target.value)}
          required
        />
        <button type="submit">Add Location</button>
      </form>

      {notifications.map((msg, i) => (
        <NotificationToast
          key={i}
          message={msg}
          onClose={() =>
            setNotifications((prev) => prev.filter((_, idx) => idx !== i))
          }
        />
      ))}

      {/* LOCATIONS LIST + METEO */}
      {locations.map((loc) => (
        <div key={loc.id} className="card">
          <h3>{loc.name}</h3>
          <p>Temperature: {weather[loc.id]?.temperature}°C</p>
          <p>Condition: {weather[loc.id]?.description}</p>
        </div>
      ))}
    </div>
  );
}