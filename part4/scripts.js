// Utilities: cookies
function setCookie(name, value, days = 7) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/`;
}

function getCookie(name) {
  return document.cookie.split('; ').reduce((r, v) => {
    const parts = v.split('=');
    const key = parts.shift();
    const val = parts.join('=');
    return key === name ? decodeURIComponent(val) : r;
  }, '');
}

function deleteCookie(name) {
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`;
}

// API base setup
const API_BASE = '/api/v1';

// Auth: login
async function loginUser(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error(txt || 'Login failed');
  }
  const data = await res.json();
  if (!data.access_token) throw new Error('Token missing in response');
  setCookie('token', data.access_token);
  return data;
}

function isAuthenticated() {
  return Boolean(getCookie('token'));
}

function authHeader() {
  const token = getCookie('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Places
async function fetchPlaces() {
  const res = await fetch(`${API_BASE}/places/`, { headers: { ...authHeader() } });
  if (!res.ok) throw new Error('Failed to fetch places');
  return res.json();
}

async function fetchPlace(placeId) {
  const res = await fetch(`${API_BASE}/places/${encodeURIComponent(placeId)}`, { headers: { ...authHeader() } });
  if (!res.ok) throw new Error('Failed to fetch place');
  return res.json();
}

async function fetchReviewsForPlace(placeId) {
  const res = await fetch(`${API_BASE}/review/places/${encodeURIComponent(placeId)}/reviews`, { headers: { ...authHeader() } });
  if (!res.ok) throw new Error('Failed to fetch reviews');
  return res.json();
}

async function submitReview(placeId, text, rating) {
  const token = getCookie('token');
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${API_BASE}/review/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...authHeader() },
    body: JSON.stringify({ place_id: String(placeId), text, rating: Number(rating), user_id: 'ignored-by-api' })
  });
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || 'Failed to submit review');
  }
  return res.json();
}

// Page: login
function setupLoginPage() {
  const form = document.getElementById('login-form');
  if (!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const errorBox = document.getElementById('login-error');
    if (errorBox) errorBox.textContent = '';
    try {
      await loginUser(email, password);
      window.location.href = 'index.html';
    } catch (err) {
      if (errorBox) errorBox.textContent = err.message;
      else alert('Login failed');
    }
  });
}

// Page: index (list places + filter)
function setupIndexPage() {
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = isAuthenticated() ? 'none' : 'inline-block';

  const listContainer = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');
  if (!listContainer) return;

  let placesCache = [];

  function renderPlaces(maxPrice) {
    listContainer.innerHTML = '';
    const filtered = placesCache.filter(p => {
      if (typeof maxPrice === 'number') return Number(p.price) <= maxPrice;
      return true;
    });
    filtered.forEach(p => {
      const card = document.createElement('div');
      card.className = 'place-card';
      card.innerHTML = `
        <h3>${p.title || 'Untitled'}</h3>
        <div class="price">$${Number(p.price).toFixed(2)} / night</div>
        <p class="muted">${p.description || ''}</p>
        <a class="details-button" href="place.html?id=${encodeURIComponent(p["Place id"] || p.id || '')}">View Details</a>
      `;
      listContainer.appendChild(card);
    });
  }

  fetchPlaces()
    .then(data => {
      placesCache = Array.isArray(data) ? data : [];
      renderPlaces();
    })
    .catch(() => { listContainer.textContent = 'Failed to load places.'; });

  if (priceFilter) {
    priceFilter.addEventListener('change', (e) => {
      const val = e.target.value;
      if (val === 'All') renderPlaces();
      else renderPlaces(Number(val));
    });
  }
}

// Page: place details
function setupPlacePage() {
  const detailsContainer = document.getElementById('place-details');
  if (!detailsContainer) return;
  const url = new URL(window.location.href);
  const placeId = url.searchParams.get('id');
  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) addReviewSection.style.display = isAuthenticated() ? 'block' : 'none';

  async function load() {
    try {
      const [place, reviews] = await Promise.all([
        fetchPlace(placeId),
        fetchReviewsForPlace(placeId),
      ]);

      // Place details
      const info = document.createElement('div');
      info.className = 'place-details';
      info.innerHTML = `
        <div class="place-info">
          <h2>${place.title}</h2>
          <div class="price">$${Number(place.price).toFixed(2)} / night</div>
          <p>${place.description || ''}</p>
          <div class="muted">Host: ${place.owner ? (place.owner.first_name + ' ' + place.owner.last_name) : 'N/A'}</div>
        </div>
      `;
      detailsContainer.appendChild(info);

      // Reviews
      const reviewsWrap = document.createElement('div');
      reviewsWrap.innerHTML = '<h3>Reviews</h3>';
      (Array.isArray(reviews) ? reviews : []).forEach(r => {
        const rc = document.createElement('div');
        rc.className = 'review-card';
        rc.innerHTML = `
          <div><strong>Rating:</strong> ${Number(r.rating)}/5</div>
          <p>${r.text}</p>
          <div class="muted">User: ${r.user_id}</div>
        `;
        reviewsWrap.appendChild(rc);
      });
      detailsContainer.appendChild(reviewsWrap);
    } catch (e) {
      detailsContainer.textContent = 'Failed to load place.';
    }
  }

  load();
}

// Page: add review
function setupAddReviewPage() {
  const form = document.getElementById('review-form');
  if (!form) return;
  if (!isAuthenticated()) {
    window.location.href = 'index.html';
    return;
  }
  const url = new URL(window.location.href);
  const placeId = url.searchParams.get('id');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = document.getElementById('review-text').value.trim();
    const rating = document.getElementById('review-rating').value;
    try {
      await submitReview(placeId, text, rating);
      alert('Review submitted successfully!');
      form.reset();
    } catch (err) {
      alert('Failed to submit review');
    }
  });
}

// Boot per page
document.addEventListener('DOMContentLoaded', () => {
  setupLoginPage();
  setupIndexPage();
  setupPlacePage();
  setupAddReviewPage();
});


