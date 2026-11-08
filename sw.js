// Service Worker for Amazfit Workout Bridge
// Handles Web Share Target API (sharing images/text directly from WhatsApp/Android)

const CACHE_NAME = 'workout-bridge-v1';
const SHARED_CACHE = 'shared-content-cache';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // Handle incoming Web Share Target POST request from Android
  if (url.pathname === '/share-target' && event.request.method === 'POST') {
    event.respondWith(handleShareTarget(event.request));
    return;
  }

  // Standard network fetch
  event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});

async function handleShareTarget(request) {
  try {
    const formData = await request.formData();
    const cache = await caches.open(SHARED_CACHE);

    // Extract shared image file if present
    const imageFile = formData.get('image');
    if (imageFile && imageFile.size > 0) {
      await cache.put('/shared-image', new Response(imageFile, {
        headers: {
          'content-type': imageFile.type || 'image/png',
          'x-filename': encodeURIComponent(imageFile.name || 'shared-image.png')
        }
      }));
    }

    // Extract shared text/URL if present
    const textData = formData.get('text') || formData.get('title') || formData.get('url');
    if (textData) {
      await cache.put('/shared-text', new Response(textData));
    }

    // Redirect to main app with query param indicating shared content is ready
    return Response.redirect('/?shared=1', 303);
  } catch (err) {
    console.error('Error handling share target in Service Worker:', err);
    return Response.redirect('/?error=share_failed', 303);
  }
}
