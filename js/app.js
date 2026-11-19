
const form = document.querySelector("#consultation-form");
const statusMessage = document.querySelector("#form-status");

if (!form || !statusMessage) {
    console.error("Form or status message element not found.");
} else {
    const submitButton = form.querySelector('button[type="submit"]');

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        statusMessage.textContent = "";
        statusMessage.className = "form-status";

        const formData = {
            full_name: document.querySelector("#full-name").value.trim(),
            email: document.querySelector("#work-email").value.trim(),
            company: document.querySelector("#company").value.trim(),
            message: document.querySelector("#message").value.trim(),
            consent: document.querySelector("#consent").checked
        };

        if (
            !formData.full_name ||
            !formData.email ||
            !formData.company ||
            !formData.message
        ) {
            showMessage("Please complete all required fields.", "error");
            return;
        }

        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailPattern.test(formData.email)) {
            showMessage("Please enter a valid email address.", "error");
            return;
        }

        if (!formData.consent) {
            showMessage(
                "Please agree to be contacted about your enquiry.",
                "error"
            );
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Sending request...";

        try {
            console.log("Sending consultation request to Python backend...");

            const response = await fetch("/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const result = await response.json();

            console.log("Backend response:", response.status, result);

            if (response.status === 201 && result.status === "received") {
                showMessage(
                    `Thank you! Your consultation request was received. Reference: ${result.request_id}`,
                    "success"
                );

                form.reset();
            } else {
                showMessage(
                    result.error || "Request failed. Please try again.",
                    "error"
                );
            }

        } catch (error) {
            console.error("Backend connection error:", error);

            showMessage(
                "Unable to connect to the Python server. Please try again.",
                "error"
            );

        } finally {
            submitButton.disabled = false;
            submitButton.textContent = "Send request";
        }
    });
}

function showMessage(message, type) {
    const statusMessage = document.querySelector("#form-status");

    statusMessage.textContent = message;
    statusMessage.className = `form-status ${type}`;
}
