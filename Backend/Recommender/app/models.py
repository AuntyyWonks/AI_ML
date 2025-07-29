from pydantic import BaseModel
from typing import List, Tuple

class Crop(BaseModel):
    name: str
    temperature_range: Tuple[float, float]
    rainfall_range: Tuple[float, float]
    soil_ph_range: Tuple[float, float]
    soil_types: List[str]
    season: str
    tips: str
