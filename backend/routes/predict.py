from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.rag.pipeline import RAGPipeline
from backend.services.weather import WeatherService

router = APIRouter()
rag_pipeline = RAGPipeline()

class RAGQuery(BaseModel):
    query: str
    k: int = 3

@router.get("/weather")
async def get_weather_data(lat: float, lon: float):
    """
    Get weather summary for a specific location.
    """
    return WeatherService.get_farming_summary(lat, lon)

from backend.services.sensors import SensorService

@router.post("/rag")
async def rag_answer(query: RAGQuery):
    try:
        # Fetch current live data to provide as context
        # Hardcoding Oujda for now as per user request
        weather = WeatherService.get_farming_summary(34.68, -1.91)
        sensors = SensorService.get_current_readings()
        
        live_data_str = f"Location: {weather.get('location', {}).get('city')}\n"
        live_data_str += f"Temperature: {weather.get('temperature')}, Humidity: {weather.get('humidity')}\n"
        live_data_str += f"Precipitation: {weather.get('precipitation')}\n"
        live_data_str += "Sensors: " + ", ".join([f"{s['name']}: {s['value']}{s['unit']}" for s in sensors['sensors']])
        
        result = rag_pipeline.generate(query.query, k=query.k, live_data=live_data_str)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
