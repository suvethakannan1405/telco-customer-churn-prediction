// ==========================================
// LOGIN PAGE JAVASCRIPT
// ==========================================

const loginForm = document.getElementById("loginForm");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");

const loginError = document.getElementById("loginError");
const loginButton = document.getElementById("loginButton");
const loginButtonText = document.getElementById("loginButtonText");


// ==========================================
// BACKEND URL
// ==========================================


const API_URL = "https://telco-customer-churn-backend.onrender.com";

// ==========================================
// SHOW / HIDE PASSWORD
// ==========================================

togglePassword.addEventListener("click", function () {

    if (passwordInput.type === "password") {

        passwordInput.type = "text";

        togglePassword.textContent = "🙈";

    } else {

        passwordInput.type = "password";

        togglePassword.textContent = "👁";

    }

});


// ==========================================
// LOGIN FORM
// ==========================================

loginForm.addEventListener("submit", async function (event) {

    event.preventDefault();


    // --------------------------------------
    // Get input values
    // --------------------------------------

    const username = usernameInput.value.trim();
    const password = passwordInput.value;


    // --------------------------------------
    // Clear previous error
    // --------------------------------------

    loginError.textContent = "";
    loginError.classList.add("hidden");


    // --------------------------------------
    // Basic validation
    // --------------------------------------

    if (username === "" || password === "") {

        loginError.textContent =
            "Please enter username and password.";

        loginError.classList.remove("hidden");

        return;
    }


    // --------------------------------------
    // Loading state
    // --------------------------------------

    loginButton.disabled = true;

    loginButtonText.textContent =
        "⏳ Signing in...";


    try {

        // ----------------------------------
        // Send login request to Flask
        // ----------------------------------

        const response = await fetch(
            `${API_URL}/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                credentials: "include",

                body: JSON.stringify({
                    username: username,
                    password: password
                })
            }
        );


        const data = await response.json();


        // ----------------------------------
        // Successful login
        // ----------------------------------

        if (response.ok && data.status === "success") {

            // Store login information
            sessionStorage.setItem(
                "loggedIn",
                "true"
            );

            sessionStorage.setItem(
                "username",
                data.username
            );


            // Change button
            loginButtonText.textContent =
                "✓ Login Successful";


            // Redirect to dashboard
            setTimeout(function () {

                window.location.href =
                    "dashboard.html";

            }, 700);

        }


        // ----------------------------------
        // Invalid login
        // ----------------------------------

        else {

            loginError.textContent =
                data.message ||
                "Invalid username or password.";

            loginError.classList.remove("hidden");

            loginButton.disabled = false;

            loginButtonText.textContent =
                "🔐 Sign In";
        }

    }


    // ======================================
    // BACKEND CONNECTION ERROR
    // ======================================

    catch (error) {

        console.error(
            "Login error:",
            error
        );

        loginError.textContent =
            "Unable to connect to the backend. Make sure Flask is running.";

        loginError.classList.remove("hidden");

        loginButton.disabled = false;

        loginButtonText.textContent =
            "🔐 Sign In";
    }

});
