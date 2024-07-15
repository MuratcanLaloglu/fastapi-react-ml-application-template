import joblib

def load_model(model_name):
    return joblib.load(f"./mlmodel/{model_name}.pkl")

def load_scaler(model_name):
    return joblib.load(f"./mlmodel/Scaler{model_name[-1]}.pkl")