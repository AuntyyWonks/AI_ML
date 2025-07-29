import json
import re

with open("app/crops.json") as f:
    crops = json.load(f)

def get_crop_names():
    return [crop["name"].lower() for crop in crops]

def handle_question(message: str):
    message = message.lower()

    # Example: What crop can I grow in summer?
    if "summer" in message:
        matches = [crop for crop in crops if crop["season"].lower() == "summer"]
        return f"In summer, you can grow: {', '.join([c['name'] for c in matches])}."

    # Example: What is the best soil for tomatoes?
    for crop in crops:
        if crop["name"].lower() in message:
            return f"{crop['name']} grows well in: {', '.join(crop['soil_types'])} soil. Ideal pH: {crop['soil_ph_range']}"
    # Example: What crops can I grow in loamy soil?
    if "loamy" in message or "sandy" in message or "clay" in message:
        soil_type = re.search(r"(loamy|sandy|clay)", message)
        if soil_type:
            matches = [crop for crop in crops if soil_type.group(0) in crop["soil_types"]]
            return f"You can grow: {', '.join([c['name'] for c in matches])} in {soil_type.group(0)} soil."
        
    
    return "Sorry, I couldn't understand that. Try asking about a crop or a season."
