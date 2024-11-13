import React, { useState } from 'react';
import { fields } from './fields'; // Adjust path as needed
import './App.css'; // Import the CSS file

function App() {
    const initialFormData = fields.reduce((acc, field) => ({ ...acc, [field.name]: '' }), {});
    const [formData, setFormData] = useState(initialFormData);
    const [prediction, setPrediction] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    // const handleSubmit = async (e) => {
    //     e.preventDefault();
    //     try {
    //         const response = await fetch('http://localhost:5001/predict', {
    //             method: 'POST',
    //             headers: { 'Content-Type': 'application/json' },
    //             body: JSON.stringify(formData),
    //         });
    //         const data = await response.json();
    //         setPrediction(data.predicted_duration); // Set the prediction state
    //     } catch (error) {
    //         console.error("Error fetching prediction:", error);
    //     }
    // };

    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
          const response = await fetch('http://localhost:5001/predict', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(formData),
          });
          const data = await response.json();
          console.log(data); // Log response to check format
          setPrediction(data.predicted_duration);
      } catch (error) {
          console.error("Error fetching prediction:", error);
      }
  };

    const handleShowExample = () => {
        const exampleData = {
            "Severity": "3",
            "Distance(mi)": "0.3",
            "Temperature(F)": "72.5",
            "Wind_Chill(F)": "70.3",
            "Humidity(%)": "65",
            "Pressure(in)": "29.92",
            "Visibility(mi)": "10",
            "Wind_Speed(mph)": "5.8",
            "Precipitation(in)": "0.0",
            "Sunrise_Sunset": "0",
            "Day_Night": "0",
            "month": "5",
            "year": "2023",
            "day_of_week": "1",
            "zipcode_population": "50000"
        };
        setFormData(exampleData);
    };

    return (
        <div>
            <h1>Accident Duration Predictor</h1>
            <form onSubmit={handleSubmit}>
                {fields.map(({ name, label, type }) => (
                    <div key={name} className="form-field">
                        <label>{label}:</label>
                        <input
                            type={type}
                            name={name}
                            value={formData[name]}
                            onChange={handleChange}
                        />
                    </div>
                ))}
                <button type="submit">Predict</button>
            </form>
            <button onClick={handleShowExample} style={{ marginTop: '1em' }}>
                Show Example
            </button>
            {prediction !== null && ( // Conditionally render the prediction result
                <div style={{ marginTop: '1em' }}>
                    <h2>Predicted Duration: {prediction} mins</h2>
                </div>
            )}
        </div>
    );
}

export default App;
