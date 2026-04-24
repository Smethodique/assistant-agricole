import requests
from typing import Dict, Any, Optional

class WeatherService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    @classmethod
    def get_weather(cls, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches current weather and agricultural data for a given location.
        """
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "relative_humidity_2m", "precipitation", "weather_code"],
            "hourly": ["temperature_2m", "soil_temperature_0_to_7cm", "soil_moisture_0_to_1cm"],
            "timezone": "auto",
            "forecast_days": 1
        }
        
        try:
            response = requests.get(cls.BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

    @classmethod
    def get_city_name(cls, lat: float, lon: float) -> str:
        """
        Reverse geocoding to get city name from coordinates.
        Uses a free/no-key API for demonstration.
        """
        try:
            # Using Open-Meteo Geocoding or Nominatim (simplified for demo)
            geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
            headers = {"User-Agent": "PrecisionFarmingAssistant/1.0"}
            response = requests.get(geo_url, headers=headers, timeout=5)
            if response.status_code == 200:
                address = response.json().get("address", {})
                return address.get("city") or address.get("town") or address.get("village") or "Unknown Location"
            return "Unknown Location"
        except Exception:
            return "Unknown Location"

    @classmethod
    def get_farming_summary(cls, lat: float, lon: float) -> Dict[str, Any]:
        """
        Returns a simplified summary useful for farming recommendations.
        """
        data = cls.get_weather(lat, lon)
        if "error" in data:
            return data
            
        current = data.get("current", {})
        hourly = data.get("hourly", {})
        
        # Simple heuristic for farming context
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        precip = current.get("precipitation")
        
        # Get latest soil data if available
        soil_temp = hourly.get("soil_temperature_0_to_7cm", [None])[0]
        soil_moisture = hourly.get("soil_moisture_0_to_1cm", [None])[0]
        
        # Get city name
        city = cls.get_city_name(lat, lon)
        
        return {
            "location": {"lat": lat, "lon": lon, "city": city},
            "temperature": f"{temp}°C",
            "humidity": f"{humidity}%",
            "precipitation": f"{precip}mm",
            "soil_temperature": f"{soil_temp}°C" if soil_temp else "N/A",
            "soil_moisture": f"{soil_moisture} m³/m³" if soil_moisture else "N/A",
            "is_raining": precip > 0 if precip is not None else False
        }

if __name__ == "__main__":
    # Quick test for a sample location (e.g., San Francisco)
    service = WeatherService()
    print(service.get_farming_summary(37.7749, -122.4194))
