import numpy as np
from config import load_model, load_scaler
from app.models import InputData

class PredictionService:
    def __init__(self):
        self.model = load_model()
        self.scaler = load_scaler()

    def predict(self, input_data: InputData):
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
        scaled_x_values = self.scaler.transform(x_values)

        prediction = self.model.predict(scaled_x_values)

        return {"prediction": int(prediction[0])}