import requests
from typing import Dict, Optional, List
from app.config import settings

class SoilService:
    def __init__(self):
        self.username = settings.ISDA_USERNAME
        self.password = settings.ISDA_PASSWORD
        self.base_url = settings.SOIL_API_BASE_URL
        self.access_token = None
        self.token_expires = None
        
    def authenticate(self) -> bool:
        """
        Authenticate with iSDAsoil API and get access token
        
        Returns:
            True if authentication successful, False otherwise
        """
        if not self.username or not self.password:
            raise ValueError("iSDAsoil credentials not configured")
            
        url = f"{self.base_url}/login"
        payload = {
            "username": self.username,
            "password": self.password
        }
        
        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get("access_token")
            
            if self.access_token:
                print("Successfully authenticated with iSDAsoil API")
                return True
            else:
                print("Authentication failed: No access token received")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Soil API authentication failed: {e}")
            return False
        except Exception as e:
            print(f"Authentication processing failed: {e}")
            return False
    
    def get_soil_properties(self, lat: float, lon: float, properties: List[str] = None, depth: str = "0-20") -> Optional[Dict]:
        """
        Get soil properties for a specific location in South Africa
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            properties: List of soil properties to retrieve (None for all)
            depth: Soil depth range (e.g., "0-20", "20-50")
            
        Returns:
            Dictionary with soil property data or None if failed
        """
        # Ensure we have a valid access token
        if not self.access_token:
            if not self.authenticate():
                return None
                
        url = f"{self.base_url}/isdasoil/v2/soilproperty"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        params = {
            "lat": lat,
            "lon": lon,
            "depth": depth
        }
        
        # Add specific properties if requested
        if properties:
            params["property"] = ",".join(properties)
            
        try:
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            # Handle token expiration
            if response.status_code == 401:
                print("Access token expired, re-authenticating...")
                if self.authenticate():
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = requests.get(url, headers=headers, params=params, timeout=15)
                else:
                    return None
                    
            response.raise_for_status()
            
            data = response.json()
            
            # Process soil data for agricultural use
            soil_info = {
                "location": {
                    "latitude": lat,
                    "longitude": lon,
                    "depth": depth
                },
                "properties": {}
            }
            
            # Extract soil properties
            for prop_name, prop_data in data.items():
                if isinstance(prop_data, dict) and "value" in prop_data:
                    soil_info["properties"][prop_name] = {
                        "value": prop_data.get("value"),
                        "unit": prop_data.get("unit", ""),
                        "uncertainty": prop_data.get("uncertainty"),
                        "description": self._get_property_description(prop_name)
                    }
            
            return soil_info
            
        except requests.exceptions.RequestException as e:
            print(f"Soil API request failed: {e}")
            return None
        except Exception as e:
            print(f"Soil data processing failed: {e}")
            return None
    
    def get_available_layers(self) -> Optional[Dict]:
        """
        Get metadata about available soil property layers
        
        Returns:
            Dictionary with layer metadata or None if failed
        """
        if not self.access_token:
            if not self.authenticate():
                return None
                
        url = f"{self.base_url}/isdasoil/v2/layers"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 401:
                if self.authenticate():
                    headers["Authorization"] = f"Bearer {self.access_token}"
                    response = requests.get(url, headers=headers, timeout=10)
                else:
                    return None
                    
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Soil layers API request failed: {e}")
            return None
        except Exception as e:
            print(f"Soil layers processing failed: {e}")
            return None
    
    def get_agricultural_soil_analysis(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get comprehensive soil analysis focused on agricultural properties
        
        Args:
            lat: Latitude coordinate
            lon: Longitude coordinate
            
        Returns:
            Dictionary with agricultural soil analysis or None if failed
        """
        # Key agricultural soil properties
        agricultural_properties = [
            "ph",           # Soil pH
            "soc",          # Soil organic carbon
            "sand",         # Sand content
            "clay",         # Clay content
            "silt",         # Silt content
            "nitrogen",     # Nitrogen content
            "phosphorus",   # Phosphorus content
            "potassium",    # Potassium content
            "cec"           # Cation exchange capacity
        ]
        
        soil_data = self.get_soil_properties(lat, lon, agricultural_properties)
        
        if not soil_data:
            return None
            
        # Add agricultural interpretation
        analysis = {
            "location": soil_data["location"],
            "soil_analysis": soil_data["properties"],
            "agricultural_interpretation": self._interpret_soil_for_agriculture(soil_data["properties"])
        }
        
        return analysis
    
    def _interpret_soil_for_agriculture(self, properties: Dict) -> Dict:
        """
        Provide agricultural interpretation of soil properties
        
        Args:
            properties: Dictionary of soil properties
            
        Returns:
            Dictionary with agricultural recommendations
        """
        interpretation = {
            "soil_type": "Unknown",
            "fertility_rating": "Unknown",
            "ph_status": "Unknown",
            "organic_matter": "Unknown",
            "nutrient_status": {},
            "recommendations": []
        }
        
        # Interpret pH
        if "ph" in properties and properties["ph"]["value"]:
            ph_value = properties["ph"]["value"]
            if ph_value < 5.5:
                interpretation["ph_status"] = "Acidic - may need lime"
                interpretation["recommendations"].append("Consider soil liming to increase pH")
            elif ph_value > 7.5:
                interpretation["ph_status"] = "Alkaline - may limit nutrient availability"
                interpretation["recommendations"].append("Monitor nutrient availability in alkaline conditions")
            else:
                interpretation["ph_status"] = "Optimal for most crops"
        
        # Interpret soil texture
        sand = properties.get("sand", {}).get("value", 0)
        clay = properties.get("clay", {}).get("value", 0)
        silt = properties.get("silt", {}).get("value", 0)
        
        if sand > 70:
            interpretation["soil_type"] = "Sandy - good drainage, may need frequent irrigation"
        elif clay > 40:
            interpretation["soil_type"] = "Clay - good water retention, may have drainage issues"
        else:
            interpretation["soil_type"] = "Loamy - balanced soil type, good for most crops"
        
        # Interpret organic carbon
        if "soc" in properties and properties["soc"]["value"]:
            soc_value = properties["soc"]["value"]
            if soc_value < 1.0:
                interpretation["organic_matter"] = "Low - needs organic matter addition"
                interpretation["recommendations"].append("Add compost or organic matter to improve soil health")
            elif soc_value > 3.0:
                interpretation["organic_matter"] = "High - excellent soil health"
            else:
                interpretation["organic_matter"] = "Moderate - adequate for crop production"
        
        return interpretation
    
    def _get_property_description(self, property_name: str) -> str:
        """
        Get human-readable description for soil properties
        """
        descriptions = {
            "ph": "Soil acidity/alkalinity level",
            "soc": "Soil organic carbon content",
            "sand": "Sand particle percentage",
            "clay": "Clay particle percentage", 
            "silt": "Silt particle percentage",
            "nitrogen": "Total nitrogen content",
            "phosphorus": "Available phosphorus",
            "potassium": "Exchangeable potassium",
            "cec": "Cation exchange capacity",
            "bulk_density": "Soil bulk density",
            "carbon_stocks": "Total carbon stocks"
        }
        return descriptions.get(property_name, f"Soil property: {property_name}")

# Global soil service instance
soil_service = SoilService()