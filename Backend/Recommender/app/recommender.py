import json
from pathlib import Path
from typing import List, Dict, Optional
from app.models import Crop
from app.weather_service import weather_service
from app.soil_service import soil_service

def load_crops():
    crops_path = Path(__file__).parent / "crops.json"
    with crops_path.open() as f:
        return [Crop(**c) for c in json.load(f)]

def recommend_crops(temp, rain, ph, soil_type):
    """Original crop recommendation function (backward compatibility)"""
    crops = load_crops()
    recommendations = []
    for crop in crops:
        if (crop.temperature_range[0] <= temp <= crop.temperature_range[1] and
            crop.rainfall_range[0] <= rain <= crop.rainfall_range[1] and
            crop.soil_ph_range[0] <= ph <= crop.soil_ph_range[1] and
            soil_type.lower() in [s.lower() for s in crop.soil_types]):
            recommendations.append({
                "name": crop.name,
                "season": crop.season,
                "tips": crop.tips
            })
    return recommendations

def recommend_crops_with_location(city: str = None, lat: float = None, lon: float = None) -> Dict:
    """
    Enhanced crop recommendation using real South African weather and soil data
    
    Args:
        city: South African city name (e.g., "Cape Town, ZA")
        lat: Latitude coordinate
        lon: Longitude coordinate
        
    Returns:
        Dictionary with recommendations, weather data, and soil analysis
    """
    try:
        # Get real-time weather data
        weather_data = weather_service.get_current_weather(city=city, lat=lat, lon=lon)
        if not weather_data:
            return {
                "error": "Unable to get weather data",
                "recommendations": [],
                "weather": None,
                "soil": None
            }
        
        # Get soil data if coordinates are available
        soil_data = None
        coords = weather_data["location"]["coordinates"]
        if coords["lat"] and coords["lon"]:
            soil_data = soil_service.get_agricultural_soil_analysis(
                lat=coords["lat"], 
                lon=coords["lon"]
            )
        
        # Extract parameters for crop matching
        temp = weather_data["temperature"]["current"]
        humidity = weather_data["humidity"]
        
        # Estimate rainfall from humidity (basic approach)
        estimated_rainfall = estimate_rainfall_from_humidity(humidity)
        
        # Get soil pH from soil data or use default
        soil_ph = 6.5  # Default neutral pH
        soil_type_detected = "loamy"  # Default soil type
        
        if soil_data and soil_data.get("soil_analysis"):
            ph_data = soil_data["soil_analysis"].get("ph", {})
            if ph_data.get("value"):
                soil_ph = ph_data["value"]
            
            # Determine soil type from analysis
            interpretation = soil_data.get("agricultural_interpretation", {})
            if "Sandy" in interpretation.get("soil_type", ""):
                soil_type_detected = "sandy"
            elif "Clay" in interpretation.get("soil_type", ""):
                soil_type_detected = "clay"
            elif "Loamy" in interpretation.get("soil_type", ""):
                soil_type_detected = "loamy"
        
        # Get crop recommendations using real data
        recommendations = recommend_crops(temp, estimated_rainfall, soil_ph, soil_type_detected)
        
        # Enhance recommendations with real-time context
        enhanced_recommendations = enhance_recommendations_with_context(
            recommendations, weather_data, soil_data
        )
        
        return {
            "location": weather_data["location"]["name"],
            "recommendations": enhanced_recommendations,
            "weather": {
                "temperature": temp,
                "humidity": humidity,
                "description": weather_data["weather"]["description"],
                "estimated_rainfall": estimated_rainfall
            },
            "soil": {
                "ph": soil_ph,
                "type": soil_type_detected,
                "analysis_available": soil_data is not None
            },
            "data_sources": {
                "weather": "OpenWeatherMap",
                "soil": "iSDAsoil" if soil_data else "Default values"
            }
        }
        
    except Exception as e:
        return {
            "error": f"Recommendation service error: {str(e)}",
            "recommendations": [],
            "weather": None,
            "soil": None
        }

def estimate_rainfall_from_humidity(humidity: float) -> float:
    """
    Estimate monthly rainfall from current humidity (basic approximation)
    This is a simplified approach - in production, use historical weather data
    """
    if humidity >= 80:
        return 800  # High rainfall month
    elif humidity >= 60:
        return 600  # Moderate rainfall
    elif humidity >= 40:
        return 400  # Low-moderate rainfall
    else:
        return 300  # Low rainfall

def enhance_recommendations_with_context(
    recommendations: List[Dict], 
    weather_data: Dict, 
    soil_data: Optional[Dict]
) -> List[Dict]:
    """
    Enhance crop recommendations with real-time environmental context
    """
    enhanced = []
    
    for rec in recommendations:
        enhanced_rec = rec.copy()
        
        # Add weather-specific tips
        temp = weather_data["temperature"]["current"]
        humidity = weather_data["humidity"]
        
        weather_tips = []
        if temp > 30:
            weather_tips.append("High temperature - ensure adequate irrigation")
        elif temp < 15:
            weather_tips.append("Cool weather - consider protection for sensitive crops")
            
        if humidity > 80:
            weather_tips.append("High humidity - monitor for fungal diseases")
        elif humidity < 40:
            weather_tips.append("Low humidity - increase irrigation frequency")
        
        # Add soil-specific tips
        soil_tips = []
        if soil_data:
            interpretation = soil_data.get("agricultural_interpretation", {})
            recommendations_list = interpretation.get("recommendations", [])
            soil_tips.extend(recommendations_list)
        
        # Combine all tips
        all_tips = [enhanced_rec["tips"]]
        if weather_tips:
            all_tips.extend(weather_tips)
        if soil_tips:
            all_tips.extend(soil_tips)
            
        enhanced_rec["enhanced_tips"] = all_tips
        enhanced_rec["suitability_score"] = calculate_suitability_score(
            enhanced_rec, weather_data, soil_data
        )
        
        enhanced.append(enhanced_rec)
    
    # Sort by suitability score (highest first)
    enhanced.sort(key=lambda x: x.get("suitability_score", 0), reverse=True)
    
    return enhanced

def calculate_suitability_score(
    crop_rec: Dict, 
    weather_data: Dict, 
    soil_data: Optional[Dict]
) -> float:
    """
    Calculate a suitability score (0-100) based on current conditions
    """
    score = 50.0  # Base score
    
    # Weather factors
    temp = weather_data["temperature"]["current"]
    humidity = weather_data["humidity"]
    
    # Temperature scoring (simplified)
    if 18 <= temp <= 27:  # Optimal range for most crops
        score += 20
    elif 15 <= temp <= 30:  # Good range
        score += 10
    elif temp < 10 or temp > 35:  # Poor conditions
        score -= 20
    
    # Humidity scoring
    if 50 <= humidity <= 70:  # Optimal humidity
        score += 15
    elif humidity > 90:  # Too humid
        score -= 10
    elif humidity < 30:  # Too dry
        score -= 15
    
    # Soil factors (if available)
    if soil_data:
        soil_analysis = soil_data.get("soil_analysis", {})
        ph_data = soil_analysis.get("ph", {})
        
        if ph_data.get("value"):
            ph = ph_data["value"]
            if 6.0 <= ph <= 7.5:  # Optimal pH range
                score += 15
            elif ph < 5.0 or ph > 8.5:  # Poor pH
                score -= 15
    
    return max(0, min(100, score))  # Clamp between 0-100

def get_seasonal_recommendations(season: str, location: str = None) -> Dict:
    """
    Get season-specific recommendations enhanced with location data
    """
    crops = load_crops()
    seasonal_crops = [crop for crop in crops if crop.season.lower() == season.lower()]
    
    if not seasonal_crops:
        return {
            "season": season,
            "recommendations": [],
            "message": f"No crops found for {season} season"
        }
    
    recommendations = []
    for crop in seasonal_crops:
        rec = {
            "name": crop.name,
            "season": crop.season,
            "tips": crop.tips,
            "temperature_range": crop.temperature_range,
            "rainfall_range": crop.rainfall_range,
            "soil_ph_range": crop.soil_ph_range,
            "soil_types": crop.soil_types
        }
        recommendations.append(rec)
    
    result = {
        "season": season,
        "recommendations": recommendations,
        "location": location or "General",
        "total_crops": len(recommendations)
    }
    
    # Add location-specific context if provided
    if location:
        try:
            weather_data = weather_service.get_current_weather(city=location)
            if weather_data:
                result["current_conditions"] = {
                    "temperature": weather_data["temperature"]["current"],
                    "suitable_for_season": check_seasonal_suitability(
                        weather_data["temperature"]["current"], 
                        season
                    )
                }
        except:
            pass  # Ignore weather service errors for seasonal recommendations
    
    return result

def check_seasonal_suitability(current_temp: float, season: str) -> bool:
    """
    Check if current temperature is suitable for the given season
    """
    season_temp_ranges = {
        "spring": (15, 25),
        "summer": (20, 35),
        "autumn": (10, 25),
        "winter": (5, 20)
    }
    
    temp_range = season_temp_ranges.get(season.lower(), (10, 30))
    return temp_range[0] <= current_temp <= temp_range[1]
