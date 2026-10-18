export interface WeatherLocation {
  name: string;
  country: string;
  latitude: number;
  longitude: number;
}

export interface WeatherAdvisory {
  weather_hazard: string;
  severity: 'LOW' | 'MODERATE' | 'HIGH';
  explanation: string;
  possible_crop_consequence: string;
  actions: string[];
  limitations: string;
  source: string;
}

export interface WeatherResponse {
  location: WeatherLocation;
  temperature: number;
  feels_like?: number | null;
  humidity: number;
  rainfall?: number | null;
  wind_speed: number;
  wind_direction?: number | null;
  cloudiness?: number | null;
  pressure?: number | null;
  visibility?: number | null;
  condition: string;
  description: string;
  icon: string;
  observed_at: number;
  advisory?: WeatherAdvisory | null;
}

