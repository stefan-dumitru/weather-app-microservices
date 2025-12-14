// Weather App Service Worker v2 – HTTPS safe

self.addEventListener("push", (event) => {
  const message = event.data.text();

  self.registration.showNotification("🌦 Weather Alert", {
    body: message,
    icon: "/vite.svg",
    vibrate: [200, 100, 200],
    tag: "weather-alert"
  });
});