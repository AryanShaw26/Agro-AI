from typing import Optional
from fastapi import APIRouter, Query, HTTPException, status
from app.schemas.weather import WeatherResponse
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
async def get_current_weather(
    lat: Optional[float] = Query(None, description="Geographic latitude coordinate (-90 to 90)"),
    lon: Optional[float] = Query(None, description="Geographic longitude coordinate (-180 to 180)"),
    city: Optional[str] = Query(None, description="Manual city or region name fallback (e.g. 'Kolkata,IN')")
):
    """
    Returns normalized current weather and independent agricultural crop-protection advisory.
    Primary flow: browser geolocation coordinates (lat, lon).
    Fallback flow: manual city name or postal query.
    Note: Weather advice is strictly environmental context and does NOT alter or prove ML disease predictions.
    """
    if lat is not None and lon is not None:
        return await weather_service.get_weather_by_coords(lat, lon)
    elif city:
        return await weather_service.get_weather_by_city(city)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing location parameter. Provide either latitude & longitude coordinates (?lat=...&lon=...) or a city name (?city=...)."
        )

