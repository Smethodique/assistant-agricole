from fastapi import APIRouter
from backend.services.sensors import SensorService

router = APIRouter()

@router.get("/sensors")
async def get_sensor_data():
    return SensorService.get_current_readings()
