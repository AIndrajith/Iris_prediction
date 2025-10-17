from fastapi import FastAPI,Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import joblib
import numpy as np
import pandas as pd

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger("FastAPI Iris Predictor")
try:
    model = joblib.load("model.pkl")
except Exception as e:
    logger.error("Failed to load the model: %s",e)
    raise RuntimeError("Model loading failed.") from e


app = FastAPI()

# Mount static folder for serving staticFiles like CSS, HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

species_mapping = {0: "Iris Setosa", 1: "Iris Versicolor", 2:"Iris Virginica"}

@app.get("/")
async def home():
    try:
        # serve the home page
        with open("static/index.html","r") as file:
            return file.read()
    except Exception as e:
        logger.error("Error serving home page: %s",e)
        return HTMLResponse(content="Error loading the home page", status_code = 500)
    
@app.get("/predict", response_class = HTMLResponse)
async def predict():
    try:
        # serve the prediction page 
        with open("static/predict.html","r") as file:
            return file.read()
    except Exception as e:
        logger.error("Error serving prediction page: %s",e)
        return HTMLResponse(content="Error loading the prediction page.", status_code=500)

@app.post("/predict")
async def predict_species(
    sepal_length: float= Form(...), sepal_width: float= Form(...),
    petal_length: float= Form(...), petal_width: float= Form(...)
):

    feature_names = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    
    try:
        input_df = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]], columns=feature_names)
        logger.info("Input data received: %s", input_df)

        # Predict using the model
        prediction = model.predict(input_df)[0]

        # Get the species name
        species = species_mapping.get(prediction, "Unknown")
        logger.info("Prediction made: %s", species)

        return {
            "prediction": species
        }
    except Exception as e:
        logger.error("Error making prediction: %s",e)
        return JSONResponse(content={"error": "Failed to make a prediction"}, status_code=500)
    
    if __name__ == "__main__":
        port = int(os.getenv("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)