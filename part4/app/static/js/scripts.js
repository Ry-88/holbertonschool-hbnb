document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorEl = document.getElementById('login-error');

    function setCookie(name, value, days) {
        const date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        const expires = "; expires=" + date.toUTCString();
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }

    async function loginUser(email, password) {
        const response = await fetch('/api/v1/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        if (!response.ok) {
            const text = await response.text();
            throw new Error(text || response.statusText);
        }
        return response.json();
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            errorEl && (errorEl.style.display = 'none');
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value;

            try {
                const data = await loginUser(email, password);
                if (data && data.access_token) {
                    setCookie('token', data.access_token, 7);
                    window.location.href = '/';
                } else {
                    throw new Error('Invalid response from server');
                }
            } catch (err) {
                if (errorEl) {
                    errorEl.textContent = 'Login failed: ' + err.message;
                    errorEl.style.display = 'block';
                } else {
                    alert('Login failed: ' + err.message);
                }
            }
        });
    }
});


