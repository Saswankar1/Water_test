from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = FastAPI()

# Load the trained model from the file
try:
    with open("/Users/raj/Desktop/DVC/project/model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
        # Check if the loaded model is a RandomForestClassifier
        if not isinstance(model, RandomForestClassifier):
            raise TypeError("Loaded model is not a RandomForestClassifier")
except Exception as e:
    raise RuntimeError(f"Error loading the model: {e}")

class PredictionRequest(BaseModel):
    ph: float
    Hardness: float
    Solids: float
    Chloramines: float
    Sulfate: float
    Conductivity: float
    Organic_carbon: float
    Trihalomethanes: float
    Turbidity: float

@app.get("/")
def index():
    return "Welcome"

@app.post("/predict")
async def model_predict(request: PredictionRequest):
    try:
        # Convert request to DataFrame
        input_data = pd.DataFrame([request.dict()])
        
        # Make prediction
        prediction = model.predict(input_data)
        
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {e}")
