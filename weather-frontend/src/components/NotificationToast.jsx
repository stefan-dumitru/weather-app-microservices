import { useEffect } from "react";

export default function NotificationToast({ message, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{
      position: "fixed",
      top: 20,
      right: 20,
      background: "#ff4d4f",
      color: "white",
      padding: "12px 18px",
      borderRadius: "8px",
      boxShadow: "0 4px 10px rgba(0,0,0,.2)",
      zIndex: 9999,
      fontWeight: "bold"
    }}>
      {message}
    </div>
  );
}