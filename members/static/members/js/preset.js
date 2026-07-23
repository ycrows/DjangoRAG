document.addEventListener("DOMContentLoaded", function () {
    const savePresetButton = document.getElementById("save-preset");
    const saveModelButton = document.getElementById("save-model");

    // Optional: If you want the "Save Model" button to give user feedback
    if (saveModelButton) {
        saveModelButton.addEventListener("click", function () {
            alert("Model choice locked in! Don't forget to click 'Save Preset' at the bottom to save to the database.");
        });
    }

    // Main Save Logic
    if (savePresetButton) {
        savePresetButton.addEventListener("click", function () {
            
            // 1. Figure out which model is currently active
            let currentModel = "";
            const activeTab = document.querySelector('.card-header .nav-link.active');
            
            if (activeTab) {
                const activeTabId = activeTab.getAttribute("href");
                if (activeTabId === "#tab-eg7-0") {
                    currentModel = "openai/gpt-4o-mini";
                } else if (activeTabId === "#tab-eg7-1") {
                    currentModel = "google/gemini-2.5-flash-lite";
                } else if (activeTabId === "#tab-eg7-2") {
                    currentModel = document.getElementById("custom_model").value.trim();
                    if (!currentModel) {
                        alert("Please enter a custom model ID before saving.");
                        return; // Stop the save process if custom model is empty
                    }
                }
            }

            // 2. Build the data payload
            const presetData = {
                title: document.getElementById("title").value,
                model: currentModel, // Now properly defined in this scope!
                temperature: document.getElementById("temperature").value,
                top_p: document.getElementById("top_p").value,
                frequency_penalty: document.getElementById("frequency_penalty").value,
                presence_penalty: document.getElementById("presence_penalty").value,
                max_tokens: document.getElementById("max_tokens").value,
                stop_sequence: document.getElementById("stop_sequence").value
            };

            // 3. Send the data to the backend
            fetch("/save-preset/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(presetData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Preset saved successfully!");
                } else {
                    alert("Error: " + data.error);
                }
            })
            .catch(error => {
                console.error("Error:", error);
                alert("Something went wrong.");
            });
        });
    }
});

// Helper function for CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}