'use client';

import React, { useState } from 'react';
import { 
  CloudSun, 
  MapPin, 
  Navigation, 
  Search, 
  Droplets, 
  Wind, 
  CloudRain, 
  Gauge, 
  Cloud, 
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { WeatherResponse } from '@/types/weather';

interface WeatherCardProps {
  weather: WeatherResponse | null;
  loading: boolean;
  error?: string | null;
  onUseCurrentLocation: () => void;
  onSearchCity: (city: string) => void;
}

export default function WeatherCard({
  weather,
  loading,
  error,
  onUseCurrentLocation,
  onSearchCity,
}: WeatherCardProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [showSearch, setShowSearch] = useState(false);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      onSearchCity(searchQuery.trim());
      setShowSearch(false);
    }
  };

  const formatObservedTime = (timestamp: number) => {
    try {
      const date = new Date(timestamp * 1000);
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
    } catch {
      return 'Just now';
    }
  };

  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        {/* Card Header & Location Controls */}
        <div className="flex flex-wrap items-center justify-between gap-3 mb-5">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <CloudSun className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-base text-[#1C231F]">Local Environmental Weather</h3>
              <p className="text-[11px] text-[#6B756F]">Field-level atmospheric telemetry</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={onUseCurrentLocation}
              disabled={loading}
              title="Detect device coordinates via browser GPS"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-[#E7F0EA] hover:bg-[#d8e7dc] text-[#1F694B] text-xs font-semibold transition-colors disabled:opacity-50"
            >
              <Navigation className="w-3.5 h-3.5" />
              <span>Use My Location</span>
            </button>
            <button
              onClick={() => setShowSearch(!showSearch)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[rgba(28,35,31,0.12)] hover:bg-[#F7F5EE] text-[#1C231F] text-xs font-semibold transition-colors"
            >
              <Search className="w-3.5 h-3.5 text-[#6B756F]" />
              <span>Change City</span>
            </button>
          </div>
        </div>

        {/* City Search Bar Drawer */}
        {showSearch && (
          <form onSubmit={handleSearchSubmit} className="mb-5 p-3 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.08)] flex items-center gap-2 animate-fadeIn">
            <MapPin className="w-4 h-4 text-[#1F694B] shrink-0" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Enter city or country (e.g. Kolkata, IN or Nairobi)"
              className="bg-transparent text-xs sm:text-sm text-[#1C231F] placeholder-[#6B756F] flex-1 outline-none"
              autoFocus
            />
            <button
              type="submit"
              disabled={!searchQuery.trim() || loading}
              className="px-3 py-1 bg-[#1F694B] text-white rounded-lg text-xs font-semibold hover:bg-[#18533B] transition-colors disabled:opacity-50"
            >
              Update
            </button>
          </form>
        )}

        {/* Error message */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-[#FFF7ED] border border-[#B7791F]/30 flex items-center gap-2 text-xs text-[#7C2D12]">
            <AlertCircle className="w-4 h-4 shrink-0 text-[#B7791F]" />
            <span>{error}</span>
          </div>
        )}

        {/* Loading State */}
        {loading && !weather && (
          <div className="py-12 flex flex-col items-center justify-center space-y-2 text-[#6B756F]">
            <RefreshCw className="w-6 h-6 animate-spin text-[#1F694B]" />
            <span className="text-xs">Fetching current local weather telemetry...</span>
          </div>
        )}

        {/* Active Weather Display */}
        {weather && (
          <div className="space-y-5">
            {/* Location Banner */}
            <div className="flex items-center justify-between pb-3 border-b border-[rgba(28,35,31,0.06)]">
              <div className="flex items-center gap-1.5 text-xs text-[#1C231F] font-semibold">
                <MapPin className="w-3.5 h-3.5 text-[#1F694B]" />
                <span>{weather.location.name}, {weather.location.country}</span>
                <span className="text-[10px] text-[#6B756F] font-normal">
                  ({weather.location.latitude.toFixed(2)}°, {weather.location.longitude.toFixed(2)}°)
                </span>
              </div>
              <span className="text-[11px] text-[#6B756F]">
                Observed: {formatObservedTime(weather.observed_at)}
              </span>
            </div>

            {/* Main Temperature and Condition */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="relative w-16 h-16 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] flex items-center justify-center overflow-hidden">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={`https://openweathermap.org/img/wn/${weather.icon}@2x.png`}
                    alt={weather.description}
                    className="w-14 h-14 object-contain"
                  />
                </div>
                <div>
                  <div className="text-3xl sm:text-4xl font-extrabold text-[#1C231F] tracking-tight">
                    {Math.round(weather.temperature)}°C
                  </div>
                  <div className="text-xs font-semibold capitalize text-[#1F694B]">
                    {weather.description}
                  </div>
                </div>
              </div>

              {typeof weather.feels_like === 'number' && (
                <div className="text-right">
                  <span className="text-[11px] text-[#6B756F] block">Feels like</span>
                  <span className="text-base font-bold text-[#1C231F]">
                    {Math.round(weather.feels_like)}°C
                  </span>
                </div>
              )}
            </div>

            {/* Environmental Metric Tiles */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 pt-1">
              <div className="p-3 rounded-2xl bg-[#F7F5EE]/70 border border-[rgba(28,35,31,0.05)] space-y-1">
                <div className="flex items-center gap-1.5 text-[11px] text-[#6B756F] font-medium">
                  <Droplets className="w-3.5 h-3.5 text-[#1F694B]" />
                  <span>Humidity</span>
                </div>
                <div className="text-sm font-bold text-[#1C231F]">
                  {weather.humidity}%
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-[#F7F5EE]/70 border border-[rgba(28,35,31,0.05)] space-y-1">
                <div className="flex items-center gap-1.5 text-[11px] text-[#6B756F] font-medium">
                  <Wind className="w-3.5 h-3.5 text-[#1F694B]" />
                  <span>Wind Speed</span>
                </div>
                <div className="text-sm font-bold text-[#1C231F]">
                  {weather.wind_speed.toFixed(1)} m/s
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-[#F7F5EE]/70 border border-[rgba(28,35,31,0.05)] space-y-1">
                <div className="flex items-center gap-1.5 text-[11px] text-[#6B756F] font-medium">
                  <CloudRain className="w-3.5 h-3.5 text-[#1F694B]" />
                  <span>Precipitation</span>
                </div>
                <div className="text-sm font-bold text-[#1C231F]">
                  {weather.rainfall !== null && weather.rainfall !== undefined
                    ? `${weather.rainfall.toFixed(1)} mm`
                    : 'Not recorded'}
                </div>
              </div>

              <div className="p-3 rounded-2xl bg-[#F7F5EE]/70 border border-[rgba(28,35,31,0.05)] space-y-1">
                <div className="flex items-center gap-1.5 text-[11px] text-[#6B756F] font-medium">
                  <Cloud className="w-3.5 h-3.5 text-[#1F694B]" />
                  <span>Cloud Cover</span>
                </div>
                <div className="text-sm font-bold text-[#1C231F]">
                  {weather.cloudiness !== null && weather.cloudiness !== undefined
                    ? `${weather.cloudiness}%`
                    : '--'}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="mt-5 pt-3 border-t border-[rgba(28,35,31,0.06)] flex items-center justify-between text-[11px] text-[#6B756F]">
        <span>OpenWeather Telemetry Layer</span>
        <span className="font-medium text-[#1F694B]">Live Ambient Monitoring</span>
      </div>
    </div>
  );
}
