// Wait for the DOM to load
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault(); // Prevent default form submission

            // Get email and password from the form
            const email = document.getElementById("email").value.trim();
            const password = document.getElementById("password").value.trim();

            try {
                // Send POST request to your Flask API
                const response = await fetch("/api/v1/auth/login", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ email, password })
                });

                // Parse the response
                const data = await response.json();

                if (response.ok) {
                    // Store the JWT token in cookies (expires in 1 hour)
                    document.cookie = `jwt=${data.access_token}; path=/; max-age=3600; secure; SameSite=Lax`;

                    // Redirect to index.html
                    window.location.href = "index.html";
                } else {
                    // Show error message
                    alert(data.message || "Login failed. Please check your credentials.");
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("An error occurred while trying to log in. Please try again later.");
            }
        });
    }
});
