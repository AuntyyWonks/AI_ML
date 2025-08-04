import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Weather API Configuration
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    WEATHER_API_BASE_URL = os.getenv("WEATHER_API_BASE_URL", "https://api.openweathermap.org/data/2.5")
    
    # Soil Data API Configuration
    ISDA_USERNAME = os.getenv("ISDA_USERNAME", "")
    ISDA_PASSWORD = os.getenv("ISDA_PASSWORD", "")
    SOIL_API_BASE_URL = os.getenv("SOIL_API_BASE_URL", "https://api.isda-africa.com")
    
    # Default South African coordinates (Cape Town)
    DEFAULT_LAT = -33.9249
    DEFAULT_LON = 18.4241

settings = Settings()