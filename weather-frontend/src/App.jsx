import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Locations from "./pages/Locations";
import Weather from "./pages/Weather";
import Alerts from "./pages/Alerts";

export default function App() {
  const token = localStorage.getItem("access_token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/" />} />
        <Route path="/locations" element={token ? <Locations /> : <Navigate to="/" />} />
        <Route path="/weather" element={token ? <Weather /> : <Navigate to="/" />} />
        <Route path="/alerts" element={token ? <Alerts /> : <Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}