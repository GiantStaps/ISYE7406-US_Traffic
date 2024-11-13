import pandas as pd
import numpy as np
import joblib # to save the model
import sys

model = joblib.load('./linear_svr.joblib')

data = {
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
    'duration_minutes': [45],
    'month': [5],
    'year': [2023],
    'day_of_week': [1],
    'zipcode_population': [50000]
}

# Create DataFrame
model_input = pd.DataFrame(data)

df = pd.get_dummies(model_input, columns=['Severity', 'month', 'day_of_week', 'Sunrise_Sunset'], drop_first=True)

print(model.predict(df.to_numpy()))
sys.excepthook = sys.__excepthook__
print(sys.excepthook)