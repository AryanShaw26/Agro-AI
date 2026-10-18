import os
import json
from typing import Optional, Dict, Any, List
from app.schemas.weather import WeatherAdvisory

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(CURRENT_DIR), "data")
RULES_PATH = os.path.join(DATA_DIR, "weather_rules.json")

class WeatherImpactService:
    def __init__(self, rules_path: str = RULES_PATH):
        self.rules: List[Dict[str, Any]] = self._load_rules(rules_path)

    def _load_rules(self, path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WeatherImpactService] Error loading weather rules: {e}")
            return []

    def evaluate_weather_impact(
        self,
        temperature: float,
        humidity: int,
        wind_speed: float,
        rainfall: Optional[float] = None,
        condition: Optional[str] = None
    ) -> WeatherAdvisory:
        """
        Deterministically evaluates verified agricultural rules against current weather parameters.
        Does NOT depend on or interact with the ML disease classification model.
        """
        # Iterate through rules in priority order
        for rule in self.rules:
            conds = rule.get("conditions", {})
            if not conds:
                # Catch-all normal rule at the end
                continue

            matches = True

            # Temperature checks
            if "temperature_min" in conds and temperature < conds["temperature_min"]:
                matches = False
            if "temperature_max" in conds and temperature > conds["temperature_max"]:
                matches = False

            # Humidity checks
            if "humidity_min" in conds and humidity < conds["humidity_min"]:
                matches = False
            if "humidity_max" in conds and humidity > conds["humidity_max"]:
                matches = False

            # Rainfall checks (rainfall is None if unobserved/missing; never treat as zero)
            if "rainfall_min" in conds:
                if rainfall is None or rainfall < conds["rainfall_min"]:
                    matches = False
            if "rainfall_max" in conds:
                if rainfall is not None and rainfall > conds["rainfall_max"]:
                    matches = False

            # Wind speed checks
            if "wind_speed_min" in conds and wind_speed < conds["wind_speed_min"]:
                matches = False
            if "wind_speed_max" in conds and wind_speed > conds["wind_speed_max"]:
                matches = False

            if matches:
                return WeatherAdvisory(
                    weather_hazard=rule.get("title") or rule["hazard"].replace("_", " ").title(),
                    severity=rule["severity"],
                    explanation=rule["explanation"],
                    possible_crop_consequence=rule["possible_crop_consequence"],
                    actions=rule["actions"],
                    limitations=rule["limitations"],
                    source=rule["source"]
                )

        # Fallback to normal baseline rule if none matched
        normal_rule = next((r for r in self.rules if r.get("id") == "normal_conditions"), None)
        if normal_rule:
            return WeatherAdvisory(
                weather_hazard=normal_rule.get("title") or normal_rule["hazard"].replace("_", " ").title(),
                severity=normal_rule["severity"],
                explanation=normal_rule["explanation"],
                possible_crop_consequence=normal_rule["possible_crop_consequence"],
                actions=normal_rule["actions"],
                limitations=normal_rule["limitations"],
                source=normal_rule["source"]
            )

        # Safe programmatic baseline
        return WeatherAdvisory(
            weather_hazard="Normal Baseline Conditions",
            severity="LOW",
            explanation="Current ambient weather parameters are within normal baseline ranges.",
            possible_crop_consequence="No significant weather-related abiotic stress detected on crops.",
            actions=[
                "Maintain standard agronomic care and regular scouting",
                "Ensure regular irrigation aligned with seasonal crop requirements"
            ],
            limitations="Weather observations represent regional ambient stations; canopy microclimates may vary.",
            source="Standard Extension Agronomic Best Practices"
        )

weather_impact_service = WeatherImpactService()
