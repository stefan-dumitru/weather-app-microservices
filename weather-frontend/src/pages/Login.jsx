import { useState } from "react";
import { authApi } from "../api/authApi";
import { useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: ""
  });

  const handleLogin = async () => {
    try {
      const res = await authApi.login(form);

      // save JWT token
      localStorage.setItem("access_token", res.data.access_token);

      // redirect to dashboard
      navigate("/dashboard");

    } catch (error) {
      alert("Invalid email or password");
      console.error(error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Login</h1>

      <input
        type="email"
        placeholder="Email"
        onChange={(e) => setForm({ ...form, email: e.target.value })}
      />
      <br /><br />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <br /><br />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}