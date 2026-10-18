import time
import httpx
from typing import Optional, Dict, Tuple, Any
from fastapi import HTTPException, status

from app.core.config import settings
from app.schemas.weather import WeatherResponse, WeatherLocation
from app.services.weather_impact_service import weather_impact_service

class WeatherService:
    def __init__(self):
        # Cache format: {cache_key: (WeatherResponse, timestamp)}
        self._cache: Dict[str, Tuple[WeatherResponse, float]] = {}

    def _get_api_key(self) -> str:
        key = settings.OPENWEATHER_API_KEY
        if not key or key == "your_openweather_api_key_here":
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Weather service configuration is unavailable (OpenWeather API key not configured)."
            )
        return key

    async def get_weather_by_coords(self, lat: float, lon: float) -> WeatherResponse:
        """
        Retrieves normalized current weather for geographic coordinates from OpenWeather.
        Implements in-memory caching to respect the recommended 10-minute update interval.
        """
        # 1. Coordinate range validation
        if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid geographic coordinates: lat={lat}, lon={lon}. Lat must be between -90 and 90, lon between -180 and 180."
            )

        # 2. Check in-memory cache (approx 1.1km resolution)
        cache_key = f"{round(lat, 2)}:{round(lon, 2)}"
        now = time.time()
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if now - timestamp < settings.WEATHER_CACHE_TTL_SECONDS:
                return cached_data

        # 3. Call OpenWeather API
        api_key = self._get_api_key()
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric"
        }

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.get(url, params=params)
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Weather service request timed out. Please try again later."
            )
        except Exception as e:
            # Never leak api_key or full url in logs or errors
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Network error connecting to weather service: {type(e).__name__}"
            )

        if resp.status_code == 401:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Weather service authentication failed. Please check backend server configuration."
            )
        elif resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Weather service returned error code ({resp.status_code})."
            )

        # 4. Parse & Normalize
        data = resp.json()
        weather_res = self._normalize_weather_data(data, default_lat=lat, default_lon=lon)

        # 5. Cache response
        self._cache[cache_key] = (weather_res, now)
        return weather_res

    async def get_weather_by_city(self, query: str) -> WeatherResponse:
        """
        Fallback search for manual city or postal/ZIP query.
        """
        clean_query = query.strip()
        if not clean_query:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="City or postal code query cannot be empty."
            )

        cache_key = f"city:{clean_query.lower()}"
        now = time.time()
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if now - timestamp < settings.WEATHER_CACHE_TTL_SECONDS:
                return cached_data

        api_key = self._get_api_key()
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": clean_query,
            "appid": api_key,
            "units": "metric"
        }

        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                resp = await client.get(url, params=params)
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Weather service request timed out."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Network error connecting to weather service: {type(e).__name__}"
            )

        if resp.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Could not find weather data for location '{clean_query}'. Please check spelling or enter coordinates."
            )
        elif resp.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Weather service returned error code ({resp.status_code})."
            )

        data = resp.json()
        weather_res = self._normalize_weather_data(data)
        self._cache[cache_key] = (weather_res, now)
        return weather_res

    def _normalize_weather_data(
        self,
        data: Dict[str, Any],
        default_lat: float = 0.0,
        default_lon: float = 0.0
    ) -> WeatherResponse:
        """
        Normalizes raw OpenWeather API JSON into the stable AgroAI schema.
        Never assumes missing precipitation is 0; preserves None when unobserved.
        """
        coord = data.get("coord", {})
        lat = float(coord.get("lat", default_lat))
        lon = float(coord.get("lon", default_lon))

        loc_name = data.get("name") or "Local Field"
        country = data.get("sys", {}).get("country", "")

        main = data.get("main", {})
        temp = float(main.get("temp", 20.0))
        feels_like = float(main["feels_like"]) if "feels_like" in main else None
        humidity = int(main.get("humidity", 50))
        pressure = int(main["pressure"]) if "pressure" in main else None

        # Extract rainfall if reported (1h or 3h). If not reported, keep as None!
        rainfall: Optional[float] = None
        rain_dict = data.get("rain", {})
        if isinstance(rain_dict, dict):
            if "1h" in rain_dict:
                rainfall = float(rain_dict["1h"])
            elif "3h" in rain_dict:
                rainfall = float(rain_dict["3h"])

        wind = data.get("wind", {})
        wind_speed = float(wind.get("speed", 0.0))
        wind_direction = int(wind["deg"]) if "deg" in wind else None

        clouds = data.get("clouds", {})
        cloudiness = int(clouds["all"]) if "all" in clouds else None

        visibility = int(data["visibility"]) if "visibility" in data else None

        weather_list = data.get("weather", [{}])
        first_weather = weather_list[0] if weather_list else {}
        condition = first_weather.get("main", "Clear")
        description = first_weather.get("description", "clear sky")
        icon = first_weather.get("icon", "01d")

        observed_at = int(data.get("dt", time.time()))

        # Evaluate deterministic agricultural advisory
        advisory = weather_impact_service.evaluate_weather_impact(
            temperature=temp,
            humidity=humidity,
            wind_speed=wind_speed,
            rainfall=rainfall,
            condition=condition
        )

        return WeatherResponse(
            location=WeatherLocation(
                name=loc_name,
                country=country,
                latitude=lat,
                longitude=lon
            ),
            temperature=temp,
            feels_like=feels_like,
            humidity=humidity,
            rainfall=rainfall,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            cloudiness=cloudiness,
            pressure=pressure,
            visibility=visibility,
            condition=condition,
            description=description,
            icon=icon,
            observed_at=observed_at,
            advisory=advisory
        )

weather_service = WeatherService()

