# South African Weather & Soil Data API Setup

## 🚀 Quick Start

Your AI_ML crop recommendation system now integrates with real South African weather and soil data! Follow these steps to get started.

## 📋 Prerequisites

### Required API Keys & Accounts

1. **OpenWeatherMap API** (Free tier: 1,000 calls/day)
   - Sign up at: https://openweathermap.org/api
   - Get your free API key
   - Covers all South African cities

2. **iSDAsoil API** (Free with registration)
   - Register at: https://www.isda-africa.com/isdasoil/developer/
   - Get username and password credentials
   - Provides 30m resolution soil data for South Africa

## ⚙️ Configuration

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API credentials to `.env`:**
   ```env
   # Weather API Configuration
   OPENWEATHER_API_KEY=your_actual_api_key_here
   
   # Soil Data API Configuration  
   ISDA_USERNAME=your_isda_username_here
   ISDA_PASSWORD=your_isda_password_here
   ```

3. **Install new dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🌟 New Features

### Enhanced API Endpoints

#### 1. Location-Based Recommendations
```
GET /recommend/location?city=Cape Town, ZA
GET /recommend/location?lat=-33.9249&lon=18.4241
```

**Response includes:**
- Real-time weather data
- Soil analysis (pH, type, nutrients)
- Crop suitability scores (0-100)
- Enhanced growing tips
- Data source attribution

#### 2. Seasonal Recommendations with Location Context
```
GET /recommend/seasonal?season=summer&location=Johannesburg, ZA
```

#### 3. Smart Chatbot Queries
The chatbot now understands:
- "What's the weather in Cape Town?"
- "Soil conditions in Durban"
- "Recommend crops for Johannesburg now"
- "What can I grow in Pretoria?"

### Supported South African Cities

- Cape Town, ZA
- Johannesburg, ZA  
- Durban, ZA
- Pretoria, ZA
- Port Elizabeth, ZA
- Bloemfontein, ZA
- East London, ZA
- Pietermaritzburg, ZA

## 🧪 Testing the Integration

### 1. Test Weather Service
```bash
curl "http://localhost:8000/recommend/location?city=Cape%20Town,%20ZA"
```

### 2. Test Chatbot with Location
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "weather in Cape Town"}'
```

### 3. Test Seasonal Recommendations
```bash
curl "http://localhost:8000/recommend/seasonal?season=summer&location=Durban,%20ZA"
```

## 📊 Data Sources & Quality

### Weather Data (OpenWeatherMap)
- **Coverage**: All of South Africa
- **Update Frequency**: Every 10 minutes
- **Data Points**: Temperature, humidity, pressure, wind, precipitation
- **Accuracy**: Professional-grade meteorological data

### Soil Data (iSDAsoil)
- **Coverage**: Entire African continent including South Africa
- **Resolution**: 30 meters (highly detailed)
- **Properties**: pH, organic carbon, nutrients, texture
- **Methodology**: Machine learning predictions from 158,000+ soil samples

## 🔧 Troubleshooting

### Common Issues

**"Weather service unavailable" error:**
- Check your OpenWeatherMap API key in `.env`
- Ensure API key is activated (can take up to 2 hours)
- Verify city name format: "City Name, ZA"

**"Soil data unavailable" error:**
- Verify iSDAsoil credentials in `.env`
- Check if coordinates are within Africa
- Ensure internet connectivity for API calls

**Import errors:**
- Run `pip install -r requirements.txt`
- Restart the FastAPI server: `uvicorn app.main:app --reload`

### API Rate Limits

- **OpenWeatherMap Free**: 1,000 calls/day
- **iSDAsoil**: No published limits, but use responsibly
- Implement caching for production use

## 🎯 Example Workflows

### 1. Real-time Crop Planning
```python
# Get current conditions for Johannesburg
response = requests.get(
    "http://localhost:8000/recommend/location?city=Johannesburg, ZA"
)
data = response.json()

# Access real environmental data
temperature = data["weather"]["temperature"]
soil_ph = data["soil"]["ph"]
recommendations = data["recommendations"]
```

### 2. Conversational Agriculture
```python
# Ask the chatbot about specific locations
chat_response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What crops grow well in Cape Town right now?"}
)
```

## 📈 Performance Optimization

### Caching Recommendations
- Weather data updates every 10 minutes
- Soil data is static - cache aggressively
- Implement Redis for production caching

### Error Handling
- The system gracefully falls back to default values
- All API failures are logged for debugging
- Original functionality remains available

## 🌍 Impact

This integration transforms your crop recommendation system from using static data to leveraging:

- **Real-time environmental conditions** for accurate recommendations
- **High-resolution soil data** specific to South African growing conditions  
- **Location-aware intelligence** that understands regional differences
- **Professional agricultural data** trusted by farmers and researchers

## 🚀 Next Steps

1. **Test with your API keys** - Set up credentials and test the endpoints
2. **Explore the chatbot** - Try location-specific queries
3. **Check the enhanced recommendations** - Notice the suitability scores and enhanced tips
4. **Consider production deployment** - Add caching and monitoring for production use

Your crop recommendation system is now powered by real South African agricultural data! 🇿🇦