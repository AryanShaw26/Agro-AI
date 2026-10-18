import { WeatherResponse } from '@/types/weather';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

export async function fetchWeatherByCoords(lat: number, lon: number): Promise<WeatherResponse> {
  const url = `${API_BASE}/weather?lat=${encodeURIComponent(lat)}&lon=${encodeURIComponent(lon)}`;
  const res = await fetch(url);
  if (!res.ok) {
    let msg = `Weather fetch failed (${res.status})`;
    try {
      const err = await res.json();
      if (err.detail) msg = err.detail;
    } catch {
      // ignore
    }
    throw new Error(msg);
  }
  return res.json();
}

export async function fetchWeatherByCity(city: string): Promise<WeatherResponse> {
  const url = `${API_BASE}/weather?city=${encodeURIComponent(city.trim())}`;
  const res = await fetch(url);
  if (!res.ok) {
    let msg = `Weather fetch failed (${res.status})`;
    try {
      const err = await res.json();
      if (err.detail) msg = err.detail;
    } catch {
      // ignore
    }
    throw new Error(msg);
  }
  return res.json();
}

