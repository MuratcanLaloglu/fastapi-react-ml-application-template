import joblib

def load_model():
    return joblib.load("./mlmodel/model.pkl")

def load_scaler():
    return joblib.load("./mlmodel/Scaler.pkl")