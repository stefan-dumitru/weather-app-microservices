import { useState } from "react";
import Navbar from "../components/Navbar";
import weatherApi from "../api/weatherApi";

export default function Weather() {
  const [city, setCity] = useState("");
  const [data, setData] = useState(null);

  async function fetchWeather() {
    const res = await weatherApi.getWeather(city);
    setData(res);
  }

  return (
    <>
      <Navbar />

      <div style={{ padding: 20 }}>
        <h2>Weather</h2>

        <input
          type="text"
          placeholder="City Name"
          value={city}
          onChange={e => setCity(e.target.value)}
        />
        <button onClick={fetchWeather}>Search</button>

        {data && (
          <div style={{ marginTop: 20 }}>
            <h3>{data.city_name}</h3>
            <p>Temperature: {data.temperature}°C</p>
            <p>Condition: {data.description}</p>
            <p>Humidity: {data.humidity}%</p>
          </div>
        )}
      </div>
    </>
  );
}