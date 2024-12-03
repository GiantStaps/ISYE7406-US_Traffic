from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from predict import DurationPredicator  # Assuming your class is saved in duration_predicator.py

# Define file paths for model, scaler, and metadata
model_path = './model/linear_svr.joblib'
scaler_path = './model/standard_scalar.joblib'
feature_columns_path = './model/data_colnames.joblib'
category_info_path = './model/categorical_vars_info.joblib'

app = Flask(__name__)
CORS(app)

# Initialize the predictor
predictor = DurationPredicator(model_path, scaler_path, feature_columns_path, category_info_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    ## really gotta parse these data. Well, json..
    data = {
        'Severity': int(data['Severity']),
        'Distance(mi)': float(data['Distance(mi)']),
        'Temperature(F)': float(data['Temperature(F)']),
        'Wind_Chill(F)': float(data['Wind_Chill(F)']),
        'Humidity(%)': float(data['Humidity(%)']),
        'Pressure(in)': float(data['Pressure(in)']),
        'Visibility(mi)': float(data['Visibility(mi)']),
        'Wind_Speed(mph)': float(data['Wind_Speed(mph)']),
        'Precipitation(in)': float(data['Precipitation(in)']),
        'Sunrise_Sunset': int(data['Sunrise_Sunset']),
        'Day_Night': int(data['Day_Night']),
        'month': int(data['month']),
        'year': int(data['year']),
        'day_of_week': int(data['day_of_week']),
        'zipcode_population': int(data['zipcode_population'])
    }
    
    try:
        # Run prediction
        prediction = predictor.predict_duration(data)
        
        # Format prediction to 2 decimal places and cast to standard float
        formatted_prediction = [float(round(pred, 2)) for pred in prediction]
        
        return jsonify({"predicted_duration": formatted_prediction})
    except Exception as e:
        print("Error during prediction:", e)
        return jsonify({"error": str(e)}), 400
    
@app.route('/')
def home():
    return "Welcome to the Accident Duration Predictor API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)