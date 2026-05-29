# load the model and perform prediction on giving user input...
import pandas as pd
import numpy as np
import joblib

model = joblib.load('model.pkl') # Load the model
# print("Successfully load the model")
scaler = joblib.load('scaler.pkl') # Load the scaler

# Create a function To preprocess input data...
def preprocess_data(data):
    values = np.array(list(data.values())).reshape(1,-1) # convert dict into numpy array...
    values = scaler.transform(values)
    return values

# Function to predict the values...
def predict_student(data):
    processed_data = preprocess_data(data)
    prediction = model.predict(processed_data)
    # convert numpy values into normal float...
    pred_percentage = float(prediction.flatten()[0])
    pred_percentage = np.clip(pred_percentage,0,100)
    return round(pred_percentage,2)