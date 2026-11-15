
console.log("AUTH.JS LOADED");

// Get popup elements
const alertModal = document.getElementById("alert-modal");
const alertTitle = document.getElementById("alert-title");
const alertMessage = document.getElementById("alert-message");
const alertClose = document.getElementById("alert-close");

// Check that popup elements exist
console.log("Popup elements:", {
    modal: alertModal,
    title: alertTitle,
    message: alertMessage,
    close: alertClose
});

// Store redirect destination
let redirectAfterAlert = null;

// Display popup
function showAlert(title, message, redirect = null) {
    console.log("SHOWING POPUP:", title, message);

    alertTitle.textContent = title;
    alertMessage.textContent = message;

    redirectAfterAlert = redirect;

    alertModal.style.display = "flex";
}

// Close popup
alertClose.addEventListener("click", function() {
    console.log("POPUP CLOSED");

    alertModal.style.display = "none";

    if (redirectAfterAlert !== null) {
        window.location.href = redirectAfterAlert;
    }
});

// Get authentication forms
const authForms = document.querySelectorAll(".auth-form");

console.log("Forms found:", authForms.length);

// Handle form submissions
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
            // Send request to backend
            const response = await fetch(form.action, {
                method: "POST",
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

            // Handle failed login or registration
            if (!response.ok) {

                const title = form.id === "register-form"
                    ? "REGISTRATION ERROR"
                    : "LOGIN ERROR";

                showAlert(
                    title,
                    data.detail || "Something went wrong. Please try again."
                );

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
            if (form.id === "login-form") {
                window.location.href = "/";
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