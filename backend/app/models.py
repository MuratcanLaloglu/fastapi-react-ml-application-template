from pydantic import BaseModel

class InputData(BaseModel):
    married: float
    income: float
    education: float
    loan_amount: float
    credit_history: float