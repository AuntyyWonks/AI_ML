from fastapi import FastAPI, Query
from app.recommender import recommend_crops
from typing import List
from app import chatbot

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Crop recommender API is running"}

@app.get("/recommend")
def recommend(
    temperature: float = Query(..., description="Current average temperature in °C"),
    rainfall: float = Query(..., description="Current average rainfall in mm"),
    soil_ph: float = Query(..., description="Soil pH value"),
    soil_type: str = Query(..., description="Soil type, e.g., loamy, sandy")
):
    recommendations = recommend_crops(temperature, rainfall, soil_ph, soil_type)
    return {"recommendations": recommendations}

@app.post("/chat")
def chat(user_input: dict):
    message = user_input.get("message", "")
    response = chatbot.handle_question(message)
    return {"response": response}