import logo from './logo.svg';
import './App.css';

import React, { useState } from 'react';

function App() {
    const [formData, setFormData] = useState({
        // Initialize fields (e.g., Severity, Distance, etc.)
    });
    const [prediction, setPrediction] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch('http://localhost:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });
        const data = await response.json();
        setPrediction(data.predicted_duration);
    };

    return (
        <div>
            <h1>Accident Duration Predictor</h1>
            <form onSubmit={handleSubmit}>
                {/* Add input fields for each data item */}
                <button type="submit">Predict</button>
            </form>
            {prediction && <h2>Predicted Duration: {prediction} mins</h2>}
        </div>
    );
}

export default App;