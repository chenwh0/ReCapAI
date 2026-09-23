import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { generateRecap } from "../services/api";

import "./Dashboard.css"


function Dashboard() {
    const [audioFile, setAudioFile] = useState(null);
    const [modelName, setModelName] = useState("qwen3:1.7b");
    const [exportType, setExportType] = useState(".txt");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const handleGenerateRecap = async () => {
        if (!audioFile) {
            setError("Please select an audio file!");
            return;
        }
        setError(null);
        setLoading(true);
        try {
            const data = await generateRecap(audioFile, modelName, exportType);
            navigate("/result", {state: { result: data }});
        }
        catch (error) {
            setError(error.message);
        }
        finally {
            setLoading(false);
        }
    }
    return (
        <div className="dashboard">
            <h1>ReCapAI</h1>
            <label>
                Upload Audio
                <input type="file" accept="audio/*" onChange={(event) => {setAudioFile(event.target.files[0]); setError(null);}} />
            </label>
            <label>
                Select Model
                <select value={modelName} onChange={(event) => setModelName(event.target.value)} >
                    <option value="qwen3:1.7b">qwen3:1.7b</option>
                    <option value="llama3.1:8b">llama3.1:8b</option>
                </select>
            </label>
            <label>
                Select Recap export type
                <select value={exportType} onChange={(event) => setExportType(event.target.value)} >
                    <option value=".txt">.txt</option>
                    <option value=".pdf">.pdf</option>
                    <option value=".docx">.docx</option>
                </select>
            </label>
            {error && <p className="error">{error}</p>}
            <button onClick={handleGenerateRecap} disabled={loading}>{loading ? "Generating...": "Generate Recap"}</button>
        </div>
    );
}

export default Dashboard;