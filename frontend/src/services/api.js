const API_URL = "http://localhost:8000";
export async function checkHealth() {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
        throw new Error("Backend unavailable.");
    }
    return response.json();
}

export async function generateRecap(audioFile, modelName, exportType) {
    const formData = new FormData();
    formData.append("audio", audioFile);
    formData.append("model_name", modelName);
    formData.append("export_type", exportType);
    const response = await fetch(`${API_URL}/recap`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate recap");
    }

    return response.json();
}