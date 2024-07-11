from fastapi import FastAPI, Depends
from services.prediction_service import PredictionService
from .models import InputData

app = FastAPI()


# Dependency
def get_prediction_service():
    return PredictionService()


@app.get("/")
def read_root():
    return {"message": "fastapi is working"}


@app.post("/predict")
def predict_endpoint(
    input_data: InputData,
    prediction_service: PredictionService = Depends(get_prediction_service),
):
    return prediction_service.predict(input_data)
