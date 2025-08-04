import json
import re
from typing import Optional
from app.weather_service import weather_service
from app.soil_service import soil_service

with open("app/crops.json") as f:
    crops = json.load(f)

def get_crop_names():
    return [crop["name"].lower() for crop in crops]

def handle_question(message: str):
    message_lower = message.lower()
    
    # Weather-related queries
    if any(keyword in message_lower for keyword in ["weather", "temperature", "rain", "forecast"]):
        return handle_weather_query(message_lower)
    
    # Location-specific queries  
    if any(city in message_lower for city in ["cape town", "johannesburg", "durban", "pretoria", "port elizabeth"]):
        return handle_location_query(message_lower)
    
    # Soil-related queries
    if any(keyword in message_lower for keyword in ["soil", "ph", "nutrients", "fertility"]):
        return handle_soil_query(message_lower)
    
    # Real-time recommendation queries
    if "recommend" in message_lower and ("now" in message_lower or "current" in message_lower):
        return handle_realtime_recommendation(message_lower)

    # Original seasonal queries
    if "summer" in message_lower:
        matches = [crop for crop in crops if crop["season"].lower() == "summer"]
        return f"In summer, you can grow: {', '.join([c['name'] for c in matches])}."

    # Original crop-specific queries
    for crop in crops:
        if crop["name"].lower() in message_lower:
            return f"{crop['name']} grows well in: {', '.join(crop['soil_types'])} soil. Ideal pH: {crop['soil_ph_range']}"
    
    # Original soil type queries
    if "loamy" in message_lower or "sandy" in message_lower or "clay" in message_lower:
        soil_type = re.search(r"(loamy|sandy|clay)", message_lower)
        if soil_type:
            matches = [crop for crop in crops if soil_type.group(0) in crop["soil_types"]]
            return f"You can grow: {', '.join([c['name'] for c in matches])} in {soil_type.group(0)} soil."
    
    return "Sorry, I couldn't understand that. Try asking about weather, soil conditions, or crops for specific locations in South Africa!"

def handle_weather_query(message: str) -> str:
    """Handle weather-related questions"""
    try:
        # Extract city name if mentioned
        sa_cities = {
            "cape town": "Cape Town, ZA",
            "johannesburg": "Johannesburg, ZA", 
            "durban": "Durban, ZA",
            "pretoria": "Pretoria, ZA",
            "port elizabeth": "Port Elizabeth, ZA"
        }
        
        city = None
        for city_key, city_value in sa_cities.items():
            if city_key in message:
                city = city_value
                break
        
        if "forecast" in message:
            weather_data = weather_service.get_forecast(city=city, days=3)
        else:
            weather_data = weather_service.get_current_weather(city=city)
            
        if not weather_data:
            return "Sorry, I couldn't get current weather data. Please check your API configuration."
            
        if "forecast" in message:
            location = weather_data["location"]["name"]
            return f"Weather forecast for {location}: {len(weather_data['forecasts'])} data points available. Current conditions vary throughout the forecast period."
        else:
            location = weather_data["location"]["name"]
            temp = weather_data["temperature"]["current"]
            desc = weather_data["weather"]["description"]
            humidity = weather_data["humidity"]
            
            return f"Current weather in {location}: {temp}°C, {desc}. Humidity: {humidity}%. Good conditions for checking crop recommendations!"
            
    except Exception as e:
        return f"Weather service unavailable: {str(e)}"

def handle_location_query(message: str) -> str:
    """Handle location-specific agricultural queries"""
    try:
        # Extract coordinates for major SA cities
        city_coords = {
            "cape town": (-33.9249, 18.4241),
            "johannesburg": (-26.2041, 28.0473),
            "durban": (-29.8587, 31.0218),
            "pretoria": (-25.7479, 28.2293),
            "port elizabeth": (-33.9608, 25.6022)
        }
        
        city_name = None
        coords = None
        
        for city in city_coords:
            if city in message:
                city_name = city.title()
                coords = city_coords[city]
                break
        
        if not coords:
            return "Please specify a South African city (Cape Town, Johannesburg, Durban, Pretoria, or Port Elizabeth)."
        
        # Get weather and soil data
        weather_data = weather_service.get_current_weather(lat=coords[0], lon=coords[1])
        soil_data = soil_service.get_agricultural_soil_analysis(lat=coords[0], lon=coords[1])
        
        response = f"Agricultural conditions in {city_name}:\n"
        
        if weather_data:
            temp = weather_data["temperature"]["current"]
            humidity = weather_data["humidity"]
            response += f"🌡️ Temperature: {temp}°C, Humidity: {humidity}%\n"
        
        if soil_data:
            interpretation = soil_data.get("agricultural_interpretation", {})
            soil_type = interpretation.get("soil_type", "Unknown")
            ph_status = interpretation.get("ph_status", "Unknown")
            response += f"🌱 Soil: {soil_type}\n🧪 pH: {ph_status}"
        else:
            response += "🌱 Soil data unavailable (check API credentials)"
        
        return response
        
    except Exception as e:
        return f"Location analysis unavailable: {str(e)}"

def handle_soil_query(message: str) -> str:
    """Handle soil-related questions"""
    return "For specific soil analysis, please provide a location (e.g., 'soil conditions in Cape Town'). I can analyze pH, nutrients, and soil type using real South African soil data!"

def handle_realtime_recommendation(message: str) -> str:
    """Handle real-time crop recommendation requests"""
    return "For real-time recommendations, please provide your location (e.g., 'recommend crops for Cape Town now'). I'll use current weather and soil data to suggest the best crops!"

def extract_coordinates_from_message(message: str) -> Optional[tuple]:
    """Extract latitude and longitude from message if provided"""
    # Look for coordinate patterns like "lat: -33.9, lon: 18.4"
    coord_pattern = r"lat:?\s*(-?\d+\.?\d*),?\s*lon:?\s*(-?\d+\.?\d*)"
    match = re.search(coord_pattern, message.lower())
    
    if match:
        try:
            lat = float(match.group(1))
            lon = float(match.group(2))
            return (lat, lon)
        except ValueError:
            pass
    
    return None
