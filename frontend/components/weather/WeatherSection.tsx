'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Info, MapPin, Navigation, AlertCircle, X, CheckCircle2 } from 'lucide-react';
import { WeatherResponse } from '@/types/weather';
import { fetchWeatherByCoords, fetchWeatherByCity } from '@/lib/weatherApi';
import WeatherCard from './WeatherCard';
import WeatherImpactCard from './WeatherImpactCard';
import WeatherProtectionCard from './WeatherProtectionCard';

interface WeatherSectionProps {
  customBannerText?: string;
  showTitle?: boolean;
}

export default function WeatherSection({
  customBannerText,
  showTitle = false,
}: WeatherSectionProps) {
  const [weather, setWeather] = useState<WeatherResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [locationNotice, setLocationNotice] = useState<{
    type: 'success' | 'info' | 'warning';
    message: string;
  } | null>(null);

  const loadWeatherByCoords = useCallback(async (lat: number, lon: number) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchWeatherByCoords(lat, lon);
      setWeather(data);
      if (typeof window !== 'undefined') {
        localStorage.setItem('agroai_weather_coords', JSON.stringify({ lat, lon }));
      }
      setLocationNotice({
        type: 'success',
        message: `Live GPS location resolved: ${data.location.name}, ${data.location.country}`,
      });
    } catch (err: any) {
      setError(err.message || 'Failed to fetch weather for coordinates');
    } finally {
      setLoading(false);
    }
  }, []);

  const loadWeatherByCity = useCallback(async (city: string) => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchWeatherByCity(city);
      setWeather(data);
      if (typeof window !== 'undefined') {
        localStorage.setItem('agroai_weather_city', city);
      }
    } catch (err: any) {
      setError(err.message || `Failed to fetch weather for "${city}"`);
    } finally {
      setLoading(false);
    }
  }, []);

  const requestBrowserLocation = useCallback(() => {
    if (typeof window !== 'undefined' && 'geolocation' in navigator) {
      setLoading(true);
      setError(null);

      navigator.geolocation.getCurrentPosition(
        (pos) => {
          loadWeatherByCoords(pos.coords.latitude, pos.coords.longitude);
        },
        (err) => {
          console.warn('Geolocation error:', err.message, 'Code:', err.code);
          let userNote = 'Location access unavailable. Showing weather for default agricultural hub (Kolkata, IN).';
          if (err.code === 1) {
            userNote = 'Browser location permission was not granted. Showing weather for default hub (Kolkata, IN). You can use "Change City" or allow location in your browser address bar.';
          } else if (err.code === 3) {
            userNote = 'Location detection timed out. Showing default hub (Kolkata, IN). Click "Use My Location" to retry.';
          }

          setLocationNotice({
            type: 'warning',
            message: userNote,
          });

          // Check if previously saved city exists
          const savedCity = localStorage.getItem('agroai_weather_city');
          loadWeatherByCity(savedCity || 'Kolkata,IN');
        },
        { timeout: 9000, enableHighAccuracy: true, maximumAge: 60000 }
      );
    } else {
      setLocationNotice({
        type: 'info',
        message: 'Browser geolocation is not supported on this device. Showing default regional weather.',
      });
      loadWeatherByCity('Kolkata,IN');
    }
  }, [loadWeatherByCoords, loadWeatherByCity]);

  // Initial load: Attempt browser geolocation automatically
  useEffect(() => {
    requestBrowserLocation();
  }, [requestBrowserLocation]);

  return (
    <div className="w-full space-y-6 pt-4 animate-fadeIn">
      {/* Optional Title */}
      {showTitle && (
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E7F0EA] text-xs font-semibold text-[#1F694B]">
            <MapPin className="w-3.5 h-3.5" />
            <span>Environmental Telemetry</span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#1C231F] tracking-tight">
            Weather Intelligence & Crop Protection
          </h2>
          <p className="text-xs sm:text-sm text-[#6B756F]">
            Live atmospheric monitoring paired with deterministic agronomic protective guidelines.
          </p>
        </div>
      )}

      {/* Mandated Independent Advisory Separation Banner */}
      <div className="p-4 sm:p-5 rounded-2xl bg-[#E7F0EA]/80 border border-[#1F694B]/20 flex items-start sm:items-center gap-3.5 shadow-sm">
        <div className="w-9 h-9 rounded-xl bg-[#1F694B] text-white flex items-center justify-center shrink-0">
          <Info className="w-5 h-5 text-[#D6A434]" />
        </div>
        <div className="space-y-0.5">
          <div className="text-xs font-bold uppercase tracking-wider text-[#1F694B]">
            Environmental Weather Intelligence
          </div>
          <p className="text-xs sm:text-sm text-[#1C231F] font-medium leading-relaxed">
            {customBannerText ||
              'This section is about the current weather around you. It is separate from the disease detected in your leaf image.'}
          </p>
        </div>
      </div>

      {/* Geolocation Status Notice (Dismissible) */}
      {locationNotice && (
        <div
          className={`p-3.5 rounded-2xl flex items-center justify-between text-xs transition-all ${
            locationNotice.type === 'success'
              ? 'bg-[#E7F0EA] border border-[#1F694B]/20 text-[#1F694B]'
              : 'bg-[#FFF7ED] border border-[#B7791F]/30 text-[#7C2D12]'
          }`}
        >
          <div className="flex items-center gap-2">
            {locationNotice.type === 'success' ? (
              <CheckCircle2 className="w-4 h-4 shrink-0 text-[#1F694B]" />
            ) : (
              <AlertCircle className="w-4 h-4 shrink-0 text-[#B7791F]" />
            )}
            <span>{locationNotice.message}</span>
          </div>

          <div className="flex items-center gap-2">
            {locationNotice.type === 'warning' && (
              <button
                type="button"
                onClick={requestBrowserLocation}
                className="px-2.5 py-1 rounded-lg bg-white border border-[#B7791F]/30 text-[#7C2D12] text-[11px] font-bold hover:bg-gray-50 transition-colors"
              >
                Retry GPS
              </button>
            )}
            <button
              type="button"
              onClick={() => setLocationNotice(null)}
              className="text-[#6B756F] hover:text-[#1C231F] p-1"
              aria-label="Dismiss notice"
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* 3-Card Bento Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <WeatherCard
          weather={weather}
          loading={loading}
          error={error}
          onUseCurrentLocation={requestBrowserLocation}
          onSearchCity={loadWeatherByCity}
        />

        <WeatherImpactCard
          advisory={weather?.advisory}
          loading={loading}
        />

        <WeatherProtectionCard
          advisory={weather?.advisory}
          loading={loading}
        />
      </div>
    </div>
  );
}
