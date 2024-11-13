from flask import Flask, request, jsonify
import joblib
from predict import DurationPredictor  # Assuming your class is saved in duration_predictor.py

# Define file paths for model, scaler, and metadata
model_path = '../model/linear_svr.joblib'
scaler_path = '../model/standard_scalar.joblib'
feature_columns_path = '../model/data_colnames.joblib'
category_info_path = '../model/categorical_vars_info.joblib'

app = Flask(__name__)

# Initialize the predictor
predictor = DurationPredictor(model_path, scaler_path, feature_columns_path, category_info_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    prediction = predictor.predict_duration(data)
    return jsonify({"predicted_duration": prediction.tolist()})  # Convert numpy array to list for JSON serialization

if __name__ == "__main__":
    app.run(debug=True)