from fastapi import FastAPI, Query, HTTPException
from app.recommender import recommend_crops, recommend_crops_with_location, get_seasonal_recommendations
from typing import List, Optional
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

@app.get("/recommend/location")
def recommend_by_location(
    city: Optional[str] = Query(None, description="South African city name (e.g., 'Cape Town, ZA')"),
    lat: Optional[float] = Query(None, description="Latitude coordinate"),
    lon: Optional[float] = Query(None, description="Longitude coordinate")
):
    """
    Get crop recommendations using real-time South African weather and soil data
    """
    if not city and (lat is None or lon is None):
        raise HTTPException(
            status_code=400, 
            detail="Provide either city name or latitude/longitude coordinates"
        )
    
    result = recommend_crops_with_location(city=city, lat=lat, lon=lon)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result

@app.get("/recommend/seasonal")
def recommend_seasonal(
    season: str = Query(..., description="Season: spring, summer, autumn, winter"),
    location: Optional[str] = Query(None, description="South African city for context")
):
    """
    Get season-specific crop recommendations with optional location context
    """
    valid_seasons = ["spring", "summer", "autumn", "winter"]
    if season.lower() not in valid_seasons:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid season. Choose from: {', '.join(valid_seasons)}"
        )
    
    result = get_seasonal_recommendations(season, location)
    return result

@app.post("/chat")
def chat(user_input: dict):
    message = user_input.get("message", "")
    response = chatbot.handle_question(message)
    return {"response": response}