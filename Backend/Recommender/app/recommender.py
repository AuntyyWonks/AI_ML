import json
from pathlib import Path
from app.models import Crop

def load_crops():
    crops_path = Path(__file__).parent / "crops.json"
    with crops_path.open() as f:
        return [Crop(**c) for c in json.load(f)]

def recommend_crops(temp, rain, ph, soil_type):
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
