self.addEventListener("install", function (e) {
  console.log("Service Worker instalado.");
  e.waitUntil(self.skipWaiting());
});

self.addEventListener("activate", function (e) {
  console.log("Service Worker ativado.");
  e.waitUntil(self.clients.claim());
});
