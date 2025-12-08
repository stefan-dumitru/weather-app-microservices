import { Link, useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <nav style={{
      display: "flex",
      justifyContent: "space-between",
      padding: "10px 20px",
      background: "#1e90ff",
      color: "white"
    }}>
      <div>
        <Link to="/dashboard" style={{ marginRight: 15, color: "white" }}>Dashboard</Link>
        <Link to="/locations" style={{ marginRight: 15, color: "white" }}>Locations</Link>
        <Link to="/weather" style={{ marginRight: 15, color: "white" }}>Weather</Link>
        <Link to="/alerts" style={{ color: "white" }}>Alerts</Link>
      </div>

      <button onClick={handleLogout} style={{ background: "white", color: "#1e90ff", padding: "5px 10px" }}>
        Logout
      </button>
    </nav>
  );
}