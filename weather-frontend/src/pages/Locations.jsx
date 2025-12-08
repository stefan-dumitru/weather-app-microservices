import { useEffect, useState } from "react";
import locationApi from "../api/locationApi";

export default function Locations() {
  const [locations, setLocations] = useState([]);
  const [form, setForm] = useState({
    name: "",
    latitude: "",
    longitude: "",
  });

  const [editMode, setEditMode] = useState(null);

  async function load() {
    const res = await locationApi.getLocations();
    setLocations(res.data);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleAdd(e) {
    e.preventDefault();
    await locationApi.addLocation({
      name: form.name,
      latitude: Number(form.latitude),
      longitude: Number(form.longitude)
    });
    setForm({ name: "", latitude: "", longitude: "" });
    load();
  }

  async function handleDelete(id) {
    await locationApi.deleteLocation(id);
    load();
  }

  async function handleEdit(e) {
    e.preventDefault();
    await locationApi.updateLocation(editMode, {
      name: form.name,
      latitude: Number(form.latitude),
      longitude: Number(form.longitude)
    });
    setEditMode(null);
    setForm({ name: "", latitude: "", longitude: "" });
    load();
  }

  function startEdit(loc) {
    setEditMode(loc.id);
    setForm({
      name: loc.name,
      latitude: loc.latitude,
      longitude: loc.longitude
    });
  }

  return (
    <div style={{ padding: 20 }}>
      <h2>Your Saved Locations</h2>

      <form onSubmit={editMode ? handleEdit : handleAdd}>
        <input
          type="text"
          placeholder="City Name"
          value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })}
        />
        <input
          type="number"
          placeholder="Latitude"
          value={form.latitude}
          onChange={e => setForm({ ...form, latitude: e.target.value })}
        />
        <input
          type="number"
          placeholder="Longitude"
          value={form.longitude}
          onChange={e => setForm({ ...form, longitude: e.target.value })}
        />

        <button type="submit">
          {editMode ? "Save Changes" : "Add Location"}
        </button>
      </form>

      <ul>
        {locations.map(loc => (
          <li key={loc.id}>
            <b>{loc.name}</b> ({loc.latitude}, {loc.longitude})
            <button onClick={() => startEdit(loc)}>Edit</button>
            <button onClick={() => handleDelete(loc.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}