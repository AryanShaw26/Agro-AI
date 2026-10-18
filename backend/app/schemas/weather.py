from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class WeatherLocation(BaseModel):
    name: str = Field(..., description="Resolved city or region name")
    country: str = Field(..., description="ISO 3166 country code")
    latitude: float = Field(..., description="Geographic latitude coordinate")
    longitude: float = Field(..., description="Geographic longitude coordinate")

class WeatherAdvisory(BaseModel):
    weather_hazard: str = Field(..., description="Classified weather hazard category")
    severity: Literal["LOW", "MODERATE", "HIGH"] = Field(..., description="Agricultural risk severity")
    explanation: str = Field(..., description="Plain-language scientific explanation of the environmental condition")
    possible_crop_consequence: str = Field(..., description="Specific crop physiology or stress consequence")
    actions: List[str] = Field(..., description="Actionable, verified crop protective management steps")
    limitations: str = Field(..., description="Boundary context clarifying environmental advisory status")
    source: str = Field(..., description="Institutional agricultural citation or extension reference")

class WeatherResponse(BaseModel):
    location: WeatherLocation
    temperature: float = Field(..., description="Ambient temperature in degrees Celsius")
    feels_like: Optional[float] = Field(None, description="Apparent temperature in degrees Celsius")
    humidity: int = Field(..., description="Relative humidity percentage (0-100)")
    rainfall: Optional[float] = Field(None, description="Precipitation volume in mm over past 1-3 hours (None if unavailable)")
    wind_speed: float = Field(..., description="Wind speed in meters per second")
    wind_direction: Optional[int] = Field(None, description="Wind meteorological direction in degrees")
    cloudiness: Optional[int] = Field(None, description="Cloud cover percentage (0-100)")
    pressure: Optional[int] = Field(None, description="Atmospheric pressure in hPa")
    visibility: Optional[int] = Field(None, description="Average visibility distance in meters")
    condition: str = Field(..., description="Primary weather condition group (e.g. Rain, Clear, Clouds)")
    description: str = Field(..., description="Detailed human-readable weather description")
    icon: str = Field(..., description="OpenWeather standardized icon code (e.g. 10d)")
    observed_at: int = Field(..., description="UTC Unix timestamp of observation")
    advisory: Optional[WeatherAdvisory] = Field(None, description="Deterministic agricultural weather advisory")

