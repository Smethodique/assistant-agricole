import random
from datetime import datetime

class SensorService:
    @staticmethod
    def get_current_readings():
        """
        Simulates real-time sensor data for farming.
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "sensors": [
                {
                    "id": "soil_moisture",
                    "name": "Soil Moisture",
                    "value": round(random.uniform(20, 60), 1),
                    "unit": "%",
                    "status": "Optimal"
                },
                {
                    "id": "soil_ph",
                    "name": "Soil pH",
                    "value": round(random.uniform(6.0, 7.5), 1),
                    "unit": "pH",
                    "status": "Neutral"
                },
                {
                    "id": "leaf_wetness",
                    "name": "Leaf Wetness",
                    "value": round(random.uniform(0, 100), 1),
                    "unit": "%",
                    "status": "Dry"
                },
                {
                    "id": "solar_radiation",
                    "name": "Solar Radiation",
                    "value": round(random.uniform(200, 1000), 1),
                    "unit": "W/m²",
                    "status": "Strong"
                }
            ]
        }
