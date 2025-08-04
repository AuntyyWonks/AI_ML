# AI_ML Project Wiki

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Backend Documentation](#backend-documentation)
4. [Frontend Documentation](#frontend-documentation)
5. [API Reference](#api-reference)
6. [Database Schema](#database-schema)
7. [Development Guide](#development-guide)
8. [Deployment Guide](#deployment-guide)
9. [Testing Guidelines](#testing-guidelines)
10. [Troubleshooting](#troubleshooting)

---

## Project Overview

### Mission Statement
The AI_ML Intelligent Crop Recommendation System aims to democratize agricultural knowledge by providing AI-powered crop recommendations and agricultural guidance to farmers, consultants, and agricultural enthusiasts worldwide.

### Core Philosophy
- **Data-Driven Agriculture**: Leverage environmental data to make informed crop selection decisions
- **Accessibility**: Provide an intuitive interface for users of all technical backgrounds
- **Educational**: Serve as a learning platform for agricultural science and AI concepts
- **Scalability**: Design for future expansion and integration with external data sources

### Target Audience
- **Primary**: Small to medium-scale farmers seeking crop diversification
- **Secondary**: Agricultural consultants and extension workers
- **Tertiary**: Students and researchers in agricultural sciences

---

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   React Frontend│◄──────────────►│  FastAPI Backend│
│                 │                 │                 │
│ - Chat Interface│                 │ - Recommender   │
│ - User Input    │                 │ - Chatbot       │
│ - Response Display│               │ - API Endpoints │
└─────────────────┘                 └─────────────────┘
                                             │
                                             ▼
                                    ┌─────────────────┐
                                    │  JSON Database  │
                                    │                 │
                                    │ - Crop Data     │
                                    │ - Environmental │
                                    │   Parameters    │
                                    └─────────────────┘
```

### Component Interaction Flow

1. **User Input**: User submits environmental parameters or chat message
2. **Frontend Processing**: React app validates and formats the request
3. **API Communication**: HTTP request sent to FastAPI backend
4. **Backend Processing**: 
   - Recommendation engine processes environmental data
   - Chatbot processes natural language queries
5. **Data Retrieval**: System queries crop database
6. **Response Generation**: Formatted response created
7. **Frontend Display**: Results rendered in user interface

---

## Backend Documentation

### Core Modules

#### 1. main.py - FastAPI Application
**Purpose**: Main application entry point and API endpoint definitions

**Key Functions**:
- `read_root()`: Health check endpoint
- `recommend()`: Crop recommendation endpoint
- `chat()`: Chatbot interaction endpoint

**Dependencies**:
- FastAPI for web framework
- Query parameters for input validation

#### 2. recommender.py - Recommendation Engine
**Purpose**: Core algorithm for matching environmental conditions to suitable crops

**Key Functions**:
- `load_crops()`: Loads crop data from JSON database
- `recommend_crops(temp, rain, ph, soil_type)`: Main recommendation algorithm

**Algorithm Logic**:
1. Load all crops from database
2. Filter crops based on environmental parameters:
   - Temperature within crop's optimal range
   - Rainfall within crop's requirements
   - Soil pH within acceptable range
   - Soil type matches crop preferences
3. Return matching crops with cultivation tips

#### 3. chatbot.py - Natural Language Processing
**Purpose**: Handles conversational queries about crops and agricultural practices

**Key Functions**:
- `get_crop_names()`: Extracts crop names for query matching
- `handle_question(message)`: Main NLP processing function

**Query Types Supported**:
- Seasonal queries: "What crops can I grow in summer?"
- Crop-specific queries: "What soil is best for tomatoes?"
- Soil-type queries: "What grows well in clay soil?"

**NLP Approach**:
- Pattern matching using regular expressions
- Keyword extraction and matching
- Context-aware response generation

#### 4. models.py - Data Models
**Purpose**: Pydantic models for type safety and data validation

**Crop Model Schema**:
```python
class Crop(BaseModel):
    name: str                           # Crop name
    temperature_range: Tuple[float, float]  # Min/max temperature (°C)
    rainfall_range: Tuple[float, float]     # Min/max rainfall (mm)
    soil_ph_range: Tuple[float, float]      # Min/max soil pH
    soil_types: List[str]                   # Compatible soil types
    season: str                             # Growing season
    tips: str                               # Cultivation advice
```

### Database Structure

#### crops.json Schema
The crop database follows this structure for each entry:

```json
{
  "name": "Crop Name",
  "temperature_range": [min_temp, max_temp],
  "rainfall_range": [min_rainfall, max_rainfall],
  "soil_ph_range": [min_ph, max_ph],
  "soil_types": ["soil_type1", "soil_type2"],
  "season": "growing_season",
  "tips": "Cultivation advice and best practices"
}
```

#### Supported Soil Types
- `loamy`: Well-draining, nutrient-rich soil
- `sandy`: Fast-draining, warm soil
- `clay`: Water-retentive, nutrient-dense soil
- `sandy loam`: Balanced drainage and nutrition
- `clay loam`: Good water retention with adequate drainage

#### Seasonal Categories
- **Spring**: March-May planting
- **Summer**: June-August growing season
- **Autumn**: September-November harvest
- **Winter**: December-February protected growing

---

## Frontend Documentation

### React Application Structure

#### App.js - Main Component
**Purpose**: Primary interface component managing chat functionality

**State Management**:
- `messages`: Array of chat messages
- `input`: Current user input text

**Key Features**:
- Real-time chat interface
- Message history management
- Error handling for API failures
- Keyboard navigation (Enter to send)

#### Styling Approach
- Inline styles for component-specific styling
- Responsive design principles
- Chat bubble interface design
- Accessible color schemes

### User Interface Design

#### Chat Interface Elements
1. **Message Container**: Scrollable area for conversation history
2. **Message Bubbles**: Differentiated styling for user vs. bot messages
3. **Input Field**: Text input with placeholder guidance
4. **Send Button**: Action trigger for message submission

#### Responsive Design Features
- Max-width container for optimal reading
- Flexible message bubble widths
- Scalable font sizes
- Mobile-friendly touch targets

---

## API Reference

### Endpoints

#### GET /
**Description**: Health check endpoint
**Response**: 
```json
{
  "message": "Crop recommender API is running"
}
```

#### GET /recommend
**Description**: Get crop recommendations based on environmental parameters

**Parameters**:
- `temperature` (float, required): Average temperature in °C
- `rainfall` (float, required): Average rainfall in mm
- `soil_ph` (float, required): Soil pH value (0-14)
- `soil_type` (string, required): Soil type classification

**Example Request**:
```
GET /recommend?temperature=25&rainfall=600&soil_ph=6.5&soil_type=loamy
```

**Example Response**:
```json
{
  "recommendations": [
    {
      "name": "Maize",
      "season": "summer",
      "tips": "Ensure full sun and avoid waterlogging."
    },
    {
      "name": "Green Beans",
      "season": "spring",
      "tips": "Avoid planting in cold or waterlogged soil."
    }
  ]
}
```

#### POST /chat
**Description**: Interactive chatbot for agricultural queries

**Request Body**:
```json
{
  "message": "What crops can I grow in summer?"
}
```

**Response**:
```json
{
  "response": "In summer, you can grow: Maize, Sweet Potatoes."
}
```

### Error Handling
- **400 Bad Request**: Invalid parameters or missing required fields
- **500 Internal Server Error**: Server processing errors
- **CORS Support**: Enabled for frontend integration

---

## Development Guide

### Setting Up Development Environment

#### Backend Development
1. **Python Environment**:
   ```bash
   cd Backend/Recommender
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Development Server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Development
1. **Node.js Setup**:
   ```bash
   cd Frontend/myfrontend
   npm install
   ```

2. **Start Development Server**:
   ```bash
   npm start
   ```

3. **Access Application**: http://localhost:3000

### Code Style Guidelines

#### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Document functions with docstrings
- Implement error handling for API endpoints

#### JavaScript (Frontend)
- Use ES6+ features (arrow functions, destructuring)
- Implement functional components with hooks
- Follow React best practices
- Maintain consistent indentation and naming

### Adding New Features

#### Adding New Crops
1. Update `crops.json` with new crop data
2. Ensure all required fields are present
3. Validate temperature, rainfall, and pH ranges
4. Test recommendations with new crop data

#### Extending Chatbot Capabilities
1. Add new pattern matching in `handle_question()`
2. Implement new query types
3. Test natural language understanding
4. Update response templates

#### API Endpoint Development
1. Define new endpoint in `main.py`
2. Implement business logic in separate module
3. Add input validation
4. Update API documentation

---

## Deployment Guide

### Docker Deployment

#### Backend Container
```bash
cd Backend/Recommender
docker build -t crop-recommender .
docker run -p 8000:8000 crop-recommender
```

#### Docker Compose Setup
```yaml
version: '3.8'
services:
  backend:
    build: ./Backend/Recommender
    ports:
      - "8000:8000"
  
  frontend:
    build: ./Frontend/myfrontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### Production Considerations

#### Backend Deployment
- Use production ASGI server (Gunicorn + Uvicorn)
- Implement environment-based configuration
- Set up logging and monitoring
- Configure CORS for production domains

#### Frontend Deployment
- Build optimized production bundle: `npm run build`
- Serve static files with nginx or CDN
- Configure API endpoint URLs for production
- Implement error boundary components

#### Security Measures
- Input validation and sanitization
- Rate limiting for API endpoints
- HTTPS configuration
- Environment variable management

---

## Testing Guidelines

### Backend Testing

#### Unit Tests
- Test recommendation algorithm accuracy
- Validate chatbot response logic
- Test data model validation
- API endpoint functionality

#### Integration Tests
- End-to-end API testing
- Database interaction testing
- Cross-module communication

#### Example Test Cases
```python
def test_crop_recommendation():
    # Test with optimal conditions for maize
    result = recommend_crops(25, 600, 6.0, "loamy")
    assert "Maize" in [crop["name"] for crop in result]

def test_chatbot_seasonal_query():
    response = handle_question("What can I grow in summer?")
    assert "summer" in response.lower()
    assert "Maize" in response or "Sweet Potatoes" in response
```

### Frontend Testing

#### Component Tests
- User interaction testing
- API integration testing
- State management validation
- Error handling verification

#### End-to-End Tests
- Complete user workflow testing
- Cross-browser compatibility
- Responsive design validation

---

## Troubleshooting

### Common Issues

#### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Ensure you're running from the correct directory and the app module is in PYTHONPATH

**Issue**: `FileNotFoundError: crops.json`
**Solution**: Verify crops.json exists in the app directory and path resolution is correct

**Issue**: CORS errors in browser
**Solution**: Configure CORS middleware in FastAPI application

#### Frontend Issues

**Issue**: API connection errors
**Solution**: 
- Verify backend server is running on correct port
- Check API endpoint URLs in frontend code
- Ensure CORS is properly configured

**Issue**: Build failures
**Solution**:
- Update Node.js and npm to latest versions
- Clear node_modules and reinstall dependencies
- Check for syntax errors in JavaScript code

#### Data Issues

**Issue**: No crop recommendations returned
**Solution**:
- Verify input parameters are within reasonable ranges
- Check crop database for matching entries
- Validate parameter types and formats

**Issue**: Chatbot not understanding queries
**Solution**:
- Review query patterns in chatbot.py
- Check for typos in crop names
- Ensure crop database is properly loaded

### Performance Optimization

#### Backend Optimization
- Implement caching for crop data loading
- Use async/await for I/O operations
- Optimize database queries
- Add request/response compression

#### Frontend Optimization
- Implement message virtualization for large chat histories
- Add loading states for better UX
- Optimize bundle size with code splitting
- Use React.memo for performance-critical components

### Debugging Tips

#### Backend Debugging
- Use FastAPI's automatic documentation at `/docs`
- Add logging statements for request/response tracking
- Use Python debugger (pdb) for complex issues
- Monitor API response times

#### Frontend Debugging
- Use React Developer Tools
- Check browser console for JavaScript errors
- Use network tab to monitor API calls
- Test with different input scenarios

---

## Future Development Roadmap

### Short-term Enhancements (1-3 months)
- Expand crop database to 50+ crops
- Implement user feedback system
- Add weather API integration
- Improve chatbot natural language understanding

### Medium-term Features (3-6 months)
- Machine learning model for yield prediction
- User authentication and personalization
- Mobile-responsive design improvements
- Multi-language support

### Long-term Vision (6+ months)
- Mobile application development
- Integration with IoT sensors
- Marketplace for agricultural products
- Advanced analytics and reporting features

### Research Opportunities
- Computer vision for crop disease identification
- Satellite imagery integration for field analysis
- Blockchain for supply chain tracking
- AI-powered pest identification and management

---

*This wiki serves as the comprehensive documentation for the AI_ML Intelligent Crop Recommendation System. For additional support or contributions, please refer to the project's main README.md file.*