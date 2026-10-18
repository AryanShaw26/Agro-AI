'use client';

import React from 'react';
import Link from 'next/link';
import { CloudSun, ArrowLeft, Scan, ShieldCheck } from 'lucide-react';
import WeatherSection from '@/components/weather/WeatherSection';

export default function WeatherPage() {
  return (
    <div className="w-full space-y-8 py-6 sm:py-10 max-w-6xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-6 border-b border-[rgba(28,35,31,0.06)]">
        <div className="space-y-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#E7F0EA] text-xs font-semibold text-[#1F694B]">
            <CloudSun className="w-3.5 h-3.5 text-[#D6A434]" />
            <span>OpenWeather Agricultural Layer</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-extrabold text-[#1C231F] tracking-tight">
            Field Weather Intelligence
          </h1>
          <p className="text-sm text-[#6B756F] max-w-2xl">
            Real-time environmental telemetry combined with deterministic agronomic protective advisories.
            Independent of AI leaf vision models.
          </p>
        </div>

        <Link
          href="/scan"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1F694B] text-white text-xs font-semibold shadow-sm hover:bg-[#18533B] transition-colors"
        >
          <Scan className="w-4 h-4 text-[#D6A434]" />
          <span>Scan a Leaf</span>
        </Link>
      </div>

      {/* Main Weather Section */}
      <WeatherSection showTitle={false} />
    </div>
  );
}

