
console.log("AUTH.JS LOADED");

// Get popup elements
const alertModal = document.getElementById("alert-modal");
const alertTitle = document.getElementById("alert-title");
const alertMessage = document.getElementById("alert-message");
const alertClose = document.getElementById("alert-close");

// Get the XSRF token from the browser's cookie
function getXsrfToken() {
    const match = document.cookie.match(/(?:^|; )xsrf_token=([^;]*)/);
    return match ? decodeURIComponent(match[1]) : null;
}

// Make sure the browser has an XSRF token
async function initializeXsrfToken() {
    let token = getXsrfToken();

    if (!token) {
        const response = await fetch("/csrf", {
            method: "GET",
            credentials: "same-origin",
            cache: "no-store"
        });

        if (!response.ok) {
            throw new Error("Could not retrieve XSRF token");
        }

        token = getXsrfToken();
    }

    if (!token) {
        throw new Error("Could not obtain XSRF token");
    }

    return token;
}

// Store redirect destination
let redirectAfterAlert = null;

// Display popup
function showAlert(title, message, redirect = null) {
    if (!alertModal || !alertTitle || !alertMessage) {
        console.error("Alert elements were not found.");
        return;
    }

    console.log("SHOWING POPUP:", title, message);

    alertTitle.textContent = title;
    alertMessage.textContent = message;

    redirectAfterAlert = redirect;
    alertModal.style.display = "flex";
}

// Close popup
if (alertClose) {
    alertClose.addEventListener("click", function() {
        console.log("POPUP CLOSED");

        if (alertModal) {
            alertModal.style.display = "none";
        }

        if (redirectAfterAlert !== null) {
            window.location.href = redirectAfterAlert;
        }
    });
}

// Get authentication forms
const authForms = document.querySelectorAll(".auth-form");

console.log("Forms found:", authForms.length);

// Handle login, registration, and room creation
authForms.forEach(form => {
    form.addEventListener("submit", async function(event) {
        console.log("FORM SUBMITTED:", form.id);

        // Prevent normal browser submission
        event.preventDefault();

        // Check registration passwords
        if (form.id === "register-form") {
            const password = form.querySelector("#password").value;
            const confirmPassword = form.querySelector("#confirm-password").value;

            if (password !== confirmPassword) {
                showAlert("PASSWORD ERROR", "Passwords do not match!");
                return;
            }
        }

        try {
            // Get the XSRF token
            const xsrfToken = await initializeXsrfToken();

            // Send request to backend
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "X-XSRF-Token": xsrfToken
                },
                body: new FormData(form)
            });

            console.log("SERVER RESPONSE STATUS:", response.status);

            // Read server response
            const responseText = await response.text();

            console.log("SERVER RESPONSE BODY:", responseText);

            let data = {};

            try {
                data = JSON.parse(responseText);
            } catch (error) {
                console.log("Response was not JSON.");
            }

            // Handle failed login, registration, or room creation
            if (!response.ok) {
                let title = "ERROR";
                let message = "Something went wrong. Please try again.";

                if (form.id === "register-form") {
                    title = "REGISTRATION ERROR";
                    message = data.detail || message;
                }
                else if (form.id === "login-form") {
                    title = "LOGIN ERROR";
                    message = data.detail || message;
                }
                else if (form.id === "create-room-form") {
                    title = "ROOM CREATION ERROR";
                    message = data.error || data.detail || message;
                }

                showAlert(title, message);
                return;
            }

            // Successful registration
            if (form.id === "register-form") {
                showAlert(
                    "ACCOUNT CREATED",
                    "Your account has been created successfully!",
                    "/login"
                );
            }

            // Successful login
            else if (form.id === "login-form") {
                showAlert(
                    "LOGIN SUCCESSFUL",
                    "",
                    "/lobby"
                );
            }

            // Successful room creation
            else if (form.id === "create-room-form") {
                showAlert(
                    "ROOM CREATED!",
                    "",
                    response.url
                );
            }

        } catch (error) {
            console.error("REQUEST FAILED:", error);

            showAlert(
                "CONNECTION ERROR",
                "Unable to connect to the server. Please try again."
            );
        }
    });
});

// Handle logout separately because it is not an .auth-form
const logoutForm = document.getElementById("logout-form");

if (logoutForm) {
    logoutForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        try {
            const xsrfToken = await initializeXsrfToken();

            const response = await fetch(logoutForm.action, {
                method: "POST",
                headers: {
                    "X-XSRF-Token": xsrfToken
                }
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else if (response.ok) {
                window.location.href = "/login";
            } else {
                console.error("Logout failed:", response.status);
                showAlert("LOGOUT ERROR", "Unable to log out. Please try again.");
            }

        } catch (error) {
            console.error("LOGOUT FAILED:", error);
            showAlert(
                "CONNECTION ERROR",
                "Unable to log out. Please try again."
            );
        }
    });
}

// Password validation
const passwordInput = document.getElementById("password");

if (passwordInput) {
    const requirements = {
        length: document.getElementById("length"),
        lowercase: document.getElementById("lowercase"),
        uppercase: document.getElementById("uppercase"),
        number: document.getElementById("number"),
        special: document.getElementById("special")
    };

    function validatePassword() {
        const password = passwordInput.value;

        const checks = {
            length: password.length >= 8,
            lowercase: /[a-z]/.test(password),
            uppercase: /[A-Z]/.test(password),
            number: /[0-9]/.test(password),
            special: /[!@#$%^&()\-_=]/.test(password)
        };

        for (const key in checks) {
            const requirement = requirements[key];

            if (!requirement) continue;

            requirement.classList.toggle("valid", checks[key]);
        }
    }

    // Set initial colors
    validatePassword();

    // Update colors while typing
    passwordInput.addEventListener("input", validatePassword);
}

// Username validation
const usernameInput = document.getElementById("username");

if (usernameInput) {
    const usernameLength = document.getElementById("username-length");
    const usernameCharacters = document.getElementById("username-characters");

    usernameInput.addEventListener("input", function() {
        const username = usernameInput.value;

        // Check username length (3-20 characters)
        if (usernameLength) {
            if (username.length >= 3 && username.length <= 20) {
                usernameLength.classList.remove("invalid");
                usernameLength.classList.add("valid");
            } else {
                usernameLength.classList.remove("valid");
                usernameLength.classList.add("invalid");
            }
        }

        // Check if username contains only alphanumeric characters
        if (usernameCharacters) {
            if (/^[a-zA-Z0-9]+$/.test(username)) {
                usernameCharacters.classList.remove("invalid");
                usernameCharacters.classList.add("valid");
            } else {
                usernameCharacters.classList.remove("valid");
                usernameCharacters.classList.add("invalid");
            }
        }
    });
}

// Room name validation
const roomNameInput = document.getElementById("roomName");
const roomNameLength = document.getElementById("roomNameLength");

if (roomNameInput && roomNameLength) {
    roomNameInput.addEventListener("input", function() {
        const roomName = roomNameInput.value;

        if (roomName.length >= 1 && roomName.length <= 20) {
            roomNameLength.classList.add("valid");
        } else {
            roomNameLength.classList.remove("valid");
        }
    });
}
