# AI_ML - Intelligent Crop Recommendation System

A comprehensive agricultural intelligence platform that combines machine learning, natural language processing, and web technologies to provide personalized crop recommendations and agricultural guidance.

## 🌱 Project Overview

This project is an AI-powered agricultural assistant designed to help farmers and agricultural enthusiasts make informed decisions about crop selection based on environmental conditions. The system provides intelligent crop recommendations and features an interactive chatbot for agricultural queries.

## ✨ Key Features

### 🎯 Smart Crop Recommendation Engine
- **Environmental Analysis**: Considers temperature, rainfall, soil pH, and soil type
- **Data-Driven Suggestions**: Uses a comprehensive crop database with optimal growing conditions
- **Season-Aware Recommendations**: Provides season-specific crop suggestions
- **Growing Tips**: Includes practical cultivation advice for each recommended crop

### 🤖 Interactive Agricultural Chatbot
- **Natural Language Processing**: Understands questions about crops, seasons, and soil types
- **Conversational Interface**: User-friendly chat experience
- **Knowledge Base**: Extensive information about various crops and growing conditions
- **Real-time Responses**: Instant answers to agricultural queries

### 🌐 Full-Stack Architecture
- **Backend API**: FastAPI-based REST API for crop recommendations and chat functionality
- **Frontend Interface**: React-based responsive web application
- **Data Management**: JSON-based crop database with structured information
- **Containerization**: Docker support for easy deployment

## 🏗️ Architecture

### Backend Components
- **FastAPI Application**: RESTful API server with endpoints for recommendations and chat
- **Recommendation Engine**: Algorithm that matches environmental conditions to suitable crops
- **Chatbot Module**: NLP-powered conversational interface
- **Data Models**: Pydantic models for type safety and data validation
- **Crop Database**: JSON-based storage with comprehensive crop information

### Frontend Components
- **React Application**: Modern, responsive user interface
- **Chat Interface**: Real-time messaging with the agricultural chatbot
- **API Integration**: Seamless communication with backend services

### Data Structure
Each crop in the database includes:
- Name and seasonal information
- Temperature range (°C)
- Rainfall requirements (mm)
- Soil pH preferences
- Compatible soil types
- Cultivation tips and best practices

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Docker (optional)

### Backend Setup
```bash
cd Backend/Recommender
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd Frontend/myfrontend
npm install
npm start
```

### Docker Deployment
```bash
cd Backend/Recommender
docker build -t crop-recommender .
docker run -p 8000:8000 crop-recommender
```

## 📚 API Documentation

### Crop Recommendation Endpoint
```
GET /recommend
Parameters:
- temperature: float (°C)
- rainfall: float (mm)
- soil_ph: float
- soil_type: string
```

### Chatbot Endpoint
```
POST /chat
Body: {"message": "your question about crops"}
```

## 🌾 Supported Crops

The system currently supports recommendations for:
- **Summer Crops**: Maize, Sweet Potatoes
- **Spring Crops**: Sorghum, Green Beans  
- **Autumn Crops**: Spinach
- **Winter Crops**: Cabbage

## 🔬 Technology Stack

### Backend
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and settings management
- **Python**: Core programming language
- **JSON**: Data storage format

### Frontend
- **React**: User interface library
- **JavaScript ES6+**: Modern JavaScript features
- **CSS3**: Styling and responsive design
- **Fetch API**: HTTP client for API communication

### DevOps
- **Docker**: Containerization platform
- **Uvicorn**: ASGI server for production deployment

## 🎯 Use Cases

1. **Farmers**: Get crop recommendations based on local environmental conditions
2. **Agricultural Consultants**: Provide data-driven advice to clients
3. **Students**: Learn about crop science and agricultural practices
4. **Researchers**: Study crop-environment relationships
5. **Hobbyist Gardeners**: Make informed decisions about home cultivation

## 🔮 Future Enhancements

- Integration with weather APIs for real-time data
- Machine learning models for yield prediction
- Marketplace integration for seed and equipment procurement
- Mobile application development
- Multi-language support
- Historical weather pattern analysis
- Pest and disease identification features

## 🤝 Contributing

This project welcomes contributions! Areas for improvement include:
- Expanding the crop database
- Enhancing the chatbot's natural language understanding
- Adding new recommendation algorithms
- Improving the user interface
- Adding test coverage

## 📄 License

This project is designed for educational and research purposes, focusing on beginner-friendly AI and ML concepts in agricultural technology.

## 🙋‍♂️ Support

For questions about agricultural recommendations or technical support, use the integrated chatbot or review the documentation in the Research directory.
