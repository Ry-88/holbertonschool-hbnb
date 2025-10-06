document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const loginError = document.getElementById('login-error');
  const loginLink = document.getElementById('login-link');

  function getToken() {
    return localStorage.getItem('access_token');
  }

  function setLoggedInUI() {
    const token = getToken();
    if (loginLink) {
      if (token) {
        loginLink.textContent = 'Logout';
        loginLink.href = '#';
        loginLink.onclick = (e) => {
          e.preventDefault();
          localStorage.removeItem('access_token');
          window.location.href = 'login.html';
        };
      } else {
        loginLink.textContent = 'Login';
        loginLink.href = 'login.html';
        loginLink.onclick = null;
      }
    }
  }

  async function loginUser(email, password) {
    try {
      const response = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: 'Login failed' }));
        throw new Error(err.error || 'Login failed');
      }

      const data = await response.json();
      if (!data.access_token) {
        throw new Error('Token not received');
      }
      localStorage.setItem('access_token', data.access_token);
      window.location.href = 'index.html';
    } catch (e) {
      if (loginError) {
        loginError.textContent = e.message || 'Login failed';
      } else {
        alert(e.message || 'Login failed');
      }
    }
  }

  if (loginForm) {
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = /** @type {HTMLInputElement} */(document.getElementById('email')).value.trim();
      const password = /** @type {HTMLInputElement} */(document.getElementById('password')).value;
      if (!email || !password) {
        if (loginError) loginError.textContent = 'Please enter email and password';
        return;
      }
      if (loginError) loginError.textContent = '';
      loginUser(email, password);
    });
  }

  setLoggedInUI();
});


