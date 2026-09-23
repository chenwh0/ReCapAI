import { useLocation } from "react-router-dom";

import "./Result.css"

function Result() {
    const { state } = useLocation();
    const result = state?.result;
    const handleDownload = () => {
        const link = document.createElement("a");
        link.href = displayResult.output_filepath;
        link.download = "recapai.txt";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };
    const testResult = {
        recap: {
            summary:
                "The professor explained the final project requirements and discussed how students should organize their teams and begin planning their projects.",
            key_points: [
                "GPU hardware is required for the final project.",
                "Students should form project teams.",
                "Teams should begin selecting a project topic.",
            ],
            tasks: [
                "Form a project team.",
                "Choose a project topic.",
                "Begin planning the project.",
            ],
            sentiment: {
                sentiment_label: "Positive",
                explanation:
                    "The professor presented the project requirements in an encouraging and constructive manner.",
            },
        },
        output_filepath: "./output_recap/recapai.txt",
    };
    const displayResult = result || testResult; // REMOVE testResult when done styling!
    
    /*if (!result) {
        return <p>No recap result.</p>
    } // UNCOMMENT when styling done*/ 
    return (
        <div className="result">
            <h1>Your Recap...</h1>
                <section>
                    <h2>Summary</h2>
                    <p>{displayResult.recap.summary}</p>
                </section>
                <section>
                    <h2>Key points</h2>
                    <ul>
                        {displayResult.recap.key_points.map((point, index) => (
                            <li key={index}>{point}</li>
                        ))}
                    </ul>
                </section>
                <section>
                    <h2>Tasks</h2>
                    <ul>
                        {displayResult.recap.tasks.map((task, index) => (
                            <li key={index}>{task}</li>
                        ))}
                    </ul>
                </section>
                <section>
                    <h2>Sentiment: {displayResult.recap.sentiment.sentiment_label}</h2>
                    <p>{displayResult.recap.sentiment.explanation}</p>
                </section>

                <p><strong>Output file:</strong> {displayResult.output_filepath}</p>
                <button onClick={handleDownload}>Download Recap</button>
        </div>
    );
}

export default Result;