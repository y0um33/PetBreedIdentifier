const fileInput = document.getElementById("fileInput");
const preview = document.getElementById("preview");
const statusBox = document.getElementById("status");
const resultsBox = document.getElementById("results");
const analyzeBtn = document.getElementById("analyzeBtn");


fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];

    if (!file) {
        return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";

    resultsBox.innerHTML = "";
    statusBox.textContent = "";
});


analyzeBtn.addEventListener("click", async () => {

    const file = fileInput.files[0];

    if (!file) {
        statusBox.textContent =
            "Please select an image first.";
        return;
    }

    try {

        statusBox.textContent = "Analyzing image...";

        const formData = new FormData();
        formData.append("file", file);

        const response = await fetch("/predict", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Request failed."
            );
        }

        let html = `
            <p>
                <strong>${data.disclaimer}</strong>
            </p>
        `;

        data.predictions.forEach(prediction => {
            html += `
                <div class="result-item">
                    ${prediction.label}
                    -
                    ${prediction.confidence}%
                </div>
            `;
        });

        resultsBox.innerHTML = html;

        statusBox.textContent =
            "Analysis completed successfully.";

    } catch (error) {

        statusBox.textContent =
            "Error: " + error.message;

        resultsBox.innerHTML = "";

    }
});