from fastapi import FastAPI
import joblib
from .models import InputData
import numpy as np

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "fastapi is working"}


@app.post("/predict")
def predict(input_data: InputData):
    model = joblib.load("./mlmodel/model.pkl")
    scaler = joblib.load("./mlmodel/Scaler.pkl")
    x_values = np.array(
        [
            [
                input_data.married,
                input_data.income,
                input_data.education,
                input_data.loan_amount,
                input_data.credit_history,
            ]
        ]
    )
    scaled_x_values = scaler.transform(x_values)

    prediction = model.predict(scaled_x_values)

    return {"prediction": int(prediction[0])}
