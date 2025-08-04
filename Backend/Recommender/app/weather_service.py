import requests
from typing import Dict, Optional
from app.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.WEATHER_API_BASE_URL
        
    def get_current_weather(self, city: str = None, lat: float = None, lon: float = None) -> Optional[Dict]:
        """
        Get current weather data for a South African location
        
        Args:
            city: City name (e.g., "Cape Town, ZA")
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Dictionary with weather data or None if failed
        """
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not configured")
            
        url = f"{self.base_url}/weather"
        params = {
            "appid": self.api_key,
            "units": "metric"  # Celsius temperature
        }
        
        # Use coordinates if provided, otherwise use city name
        if lat is not None and lon is not None:
            params.update({"lat": lat, "lon": lon})
        elif city:
            params["q"] = city
        else:
            # Default to Cape Town
            params.update({"lat": settings.DEFAULT_LAT, "lon": settings.DEFAULT_LON})
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                "location": {
                    "name": data.get("name", "Unknown"),
                    "country": data.get("sys", {}).get("country", ""),
                    "coordinates": {
                        "lat": data.get("coord", {}).get("lat"),
                        "lon": data.get("coord", {}).get("lon")
                    }
                },
                "temperature": {
                    "current": data.get("main", {}).get("temp"),
                    "feels_like": data.get("main", {}).get("feels_like"),
                    "min": data.get("main", {}).get("temp_min"),
                    "max": data.get("main", {}).get("temp_max")
                },
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "weather": {
                    "main": data.get("weather", [{}])[0].get("main"),
                    "description": data.get("weather", [{}])[0].get("description")
                },
                "wind": {
                    "speed": data.get("wind", {}).get("speed"),
                    "direction": data.get("wind", {}).get("deg")
                },
                "clouds": data.get("clouds", {}).get("all"),
                "visibility": data.get("visibility"),
                "timestamp": data.get("dt")
            }
            
            return weather_info
            
        except requests.exceptions.RequestException as e:
            print(f"Weather API request failed: {e}")
            return None
        except Exception as e:
            print(f"Weather data processing failed: {e}")
            return None
    
    def get_forecast(self, city: str = None, lat: float = None, lon: float = None, days: int = 5) -> Optional[Dict]:
        """
        Get weather forecast for a South African location
        
        Args:
            city: City name (e.g., "Cape Town, ZA")
            lat: Latitude coordinate
            lon: Longitude coordinate
            days: Number of days for forecast (max 5 for free tier)
            
        Returns:
            Dictionary with forecast data or None if failed
        """
        if not self.api_key:
            raise ValueError("OpenWeatherMap API key not configured")
            
        url = f"{self.base_url}/forecast"
        params = {
            "appid": self.api_key,
            "units": "metric"
        }
        
        # Use coordinates if provided, otherwise use city name
        if lat is not None and lon is not None:
            params.update({"lat": lat, "lon": lon})
        elif city:
            params["q"] = city
        else:
            # Default to Cape Town
            params.update({"lat": settings.DEFAULT_LAT, "lon": settings.DEFAULT_LON})
            
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data (5-day forecast with 3-hour intervals)
            forecast_info = {
                "location": {
                    "name": data.get("city", {}).get("name", "Unknown"),
                    "country": data.get("city", {}).get("country", ""),
                    "coordinates": {
                        "lat": data.get("city", {}).get("coord", {}).get("lat"),
                        "lon": data.get("city", {}).get("coord", {}).get("lon")
                    }
                },
                "forecasts": []
            }
            
            for item in data.get("list", [])[:days * 8]:  # Limit to requested days (8 entries per day)
                forecast_entry = {
                    "datetime": item.get("dt"),
                    "datetime_txt": item.get("dt_txt"),
                    "temperature": {
                        "temp": item.get("main", {}).get("temp"),
                        "feels_like": item.get("main", {}).get("feels_like"),
                        "min": item.get("main", {}).get("temp_min"),
                        "max": item.get("main", {}).get("temp_max")
                    },
                    "humidity": item.get("main", {}).get("humidity"),
                    "pressure": item.get("main", {}).get("pressure"),
                    "weather": {
                        "main": item.get("weather", [{}])[0].get("main"),
                        "description": item.get("weather", [{}])[0].get("description")
                    },
                    "wind": {
                        "speed": item.get("wind", {}).get("speed"),
                        "direction": item.get("wind", {}).get("deg")
                    },
                    "clouds": item.get("clouds", {}).get("all"),
                    "rain": item.get("rain", {}).get("3h", 0),  # 3-hour rainfall
                    "snow": item.get("snow", {}).get("3h", 0)   # 3-hour snowfall
                }
                forecast_info["forecasts"].append(forecast_entry)
                
            return forecast_info
            
        except requests.exceptions.RequestException as e:
            print(f"Weather forecast API request failed: {e}")
            return None
        except Exception as e:
            print(f"Weather forecast processing failed: {e}")
            return None

    def get_south_african_cities(self) -> list:
        """
        Return list of major South African cities for weather queries
        """
        return [
            "Cape Town, ZA",
            "Johannesburg, ZA", 
            "Durban, ZA",
            "Pretoria, ZA",
            "Port Elizabeth, ZA",
            "Bloemfontein, ZA",
            "East London, ZA",
            "Pietermaritzburg, ZA",
            "Rustenburg, ZA",
            "Polokwane, ZA"
        ]

# Global weather service instance
weather_service = WeatherService()