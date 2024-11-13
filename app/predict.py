import pandas as pd
import joblib
import numpy as np
import sys

class DurationPredictor:
    def __init__(self, model_path, scaler_path, feature_columns_path, category_info_path):
        # Load model, scaler, and metadata
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.feature_columns = joblib.load(feature_columns_path)
        self.category_info = joblib.load(category_info_path)

    def create_dataframe(self, data):
        # Create DataFrame from input data
        df = pd.DataFrame(data)
        
        # Convert categorical columns to categorical types with specified categories
        categorical_columns = ['Severity', 'month', 'year', 'day_of_week', 'Sunrise_Sunset']
        for col in categorical_columns:
            if col in data:
                df[col] = pd.Categorical(df[col], categories=self.category_info[col])
        
        # One-hot encode categorical columns and drop the first column to avoid multicollinearity
        df = pd.get_dummies(df, columns=['Severity', 'month', 'day_of_week', 'Sunrise_Sunset'], drop_first=True)
        
        # make sure all columns are present
        df = df.reindex(columns=self.feature_columns, fill_value=0)

        return df.astype('float32').to_numpy()

    def predict_duration(self, data):
        # Create processed data array
        processed_data = self.create_dataframe(data)
        
        # Scale data using the pre-fitted scaler
        scaled_data = self.scaler.transform(processed_data)
        
        # Predict duration using the pre-trained model
        prediction = self.model.predict(scaled_data)
        return prediction

# Example usage:
if __name__ == "__main__":
    # Define file paths for model, scaler, and metadata
    model_path = '../model/linear_svr.joblib'
    scaler_path = '../model/standard_scalar.joblib'
    feature_columns_path = '../model/data_colnames.joblib'
    category_info_path = '../model/categorical_vars_info.joblib'

    # Initialize the predictor
    predictor = DurationPredictor(model_path, scaler_path, feature_columns_path, category_info_path)

    # Define input data
    input_data = {
        'Severity': [3],
        'Distance(mi)': [0.3],
        'Temperature(F)': [72.5],
        'Wind_Chill(F)': [70.3],
        'Humidity(%)': [65],
        'Pressure(in)': [29.92],
        'Visibility(mi)': [10],
        'Wind_Speed(mph)': [5.8],
        'Precipitation(in)': [0.0],
        'Sunrise_Sunset': [0],
        'Day_Night': [0],
        'month': [5],
        'year': [2023],
        'day_of_week': [1],
        'zipcode_population': [50000]
    }

    # Get prediction
    prediction = predictor.predict_duration(input_data)
    print(f"Predicted Accident Duration: {prediction} mins")