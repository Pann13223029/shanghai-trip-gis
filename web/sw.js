// ============================================================
// SERVICE WORKER — Offline Caching
// ============================================================
// This caches the app shell (HTML, CSS, JS) and GeoJSON data
// so the map interface works without internet.
//
// NOTE: Map tiles are NOT cached (too large). Without internet,
// the map background will be blank but POI data and popups
// will still work. Use the PDF maps for full offline navigation.
// ============================================================

const CACHE_NAME = 'shanghai-trip-v2';

// Files to cache on install
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './css/style.css',
  './story-template.html',
  '../data/poi/landmarks.geojson',
  '../data/poi/food.geojson',
  '../data/poi/shopping.geojson',
  '../data/poi/cultural.geojson',
  '../data/poi/nature.geojson',
  '../data/poi/transport.geojson',
  '../data/poi/accommodation.geojson',
  '../data/poi/suzhou.geojson',
  '../data/routes/day-1.geojson',
  '../data/routes/day-2.geojson',
  '../data/routes/day-3.geojson',
  '../data/routes/day-4.geojson',
  '../data/routes/day-5.geojson',
  '../data/routes/day-6.geojson',
  '../data/routes/metro.geojson',
  '../data/areas/districts.geojson',
  '../data/areas/neighborhoods.geojson',
  '../data/analysis/co2-summary.json'
];

// When the service worker installs, cache all assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS_TO_CACHE))
      .then(() => self.skipWaiting())
  );
});

// When the service worker activates, clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// Serve from cache first, fall back to network
self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') return;

  // Don't cache map tiles (too large, and we have PDF fallback)
  const url = event.request.url;
  if (url.includes('tile.openstreetmap.org') ||
      url.includes('basemaps.cartocdn.com') ||
      url.includes('tiles.')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;

      return fetch(event.request).then(response => {
        // Cache successful responses for next time
        if (response.ok) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    }).catch(() => {
      // If both cache and network fail, return a simple offline message
      if (event.request.destination === 'document') {
        return new Response('<h1>Offline</h1><p>Use your PDF maps in the offline/ folder.</p>', {
          headers: { 'Content-Type': 'text/html' }
        });
      }
    })
  );
});
