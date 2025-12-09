import { useEffect } from "react";

export default function useNotifications(token, onAlert) {
  const API_GATEWAY_URL = import.meta.env.VITE_API_GATEWAY_URL;
  
  useEffect(() => {
    if (!token) return;

    const evtSource = new EventSource(
      `${API_GATEWAY_URL}/alerts/stream?token=${token}`
    );

    evtSource.onmessage = (event) => {
      console.log("🔔 SSE:", event.data);
      onAlert(event.data);
      showBrowserAlert(event.data);
    };

    evtSource.onerror = (err) => {
      console.error("SSE error:", err);
    };

    registerPush(token);

    return () => evtSource.close();
  }, [token]);
}

async function registerPush(token) {
  if (!("serviceWorker" in navigator)) {
    console.warn("❌ Service workers not supported");
    return;
  }

  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    console.warn("🚫 Push notifications denied by user");
    return;
  }

  const registration = await navigator.serviceWorker.register("/service-worker.js");

  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(import.meta.env.VITE_VAPID_PUBLIC_KEY),
  });

  // Send subscription to backend
  await fetch(`${API_GATEWAY_URL}/alerts/subscribe`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(subscription),
  });

  console.log("📡 Push subscription sent!");
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, "+")
    .replace(/_/g, "/");

  const raw = window.atob(base64);
  return Uint8Array.from([...raw].map((x) => x.charCodeAt(0)));
}

function showBrowserAlert(message) {
  if (Notification.permission === "granted") {
    new Notification("🌦 Weather Alert", {
      body: message,
      icon: "/vite.svg",
    });
  }
}