'use client';

import React from 'react';
import { ThermometerSun, AlertCircle, BookOpen, Activity } from 'lucide-react';
import { WeatherAdvisory } from '@/types/weather';

interface WeatherImpactCardProps {
  advisory?: WeatherAdvisory | null;
  loading?: boolean;
}

export default function WeatherImpactCard({ advisory, loading }: WeatherImpactCardProps) {
  if (loading && !advisory) {
    return (
      <div className="bento-card p-6 h-full flex flex-col justify-center items-center text-[#6B756F] space-y-2">
        <Activity className="w-6 h-6 animate-pulse text-[#1F694B]" />
        <span className="text-xs">Analyzing agronomic weather impact...</span>
      </div>
    );
  }

  if (!advisory) {
    return (
      <div className="bento-card p-6 h-full flex flex-col justify-between">
        <div>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <ThermometerSun className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base text-[#1C231F]">Weather Impact on Crops</h3>
          </div>
          <p className="text-xs text-[#6B756F]">
            No severe microclimatic hazards detected for current ambient readings.
          </p>
        </div>
      </div>
    );
  }

  const severityBadgeClass = {
    LOW: 'bg-[#E7F0EA] text-[#1F694B] border-[#1F694B]/20',
    MODERATE: 'bg-[#FFFBEB] text-[#B45309] border-[#B45309]/30',
    HIGH: 'bg-[#FEF2F2] text-[#B91C1C] border-[#B91C1C]/30',
  }[advisory.severity] || 'bg-gray-100 text-gray-700 border-gray-200';

  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        {/* Header with Title and Severity Badge */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <ThermometerSun className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-base text-[#1C231F]">Weather Impact on Crops</h3>
              <p className="text-[11px] text-[#6B756F]">Environmental stressor evaluation</p>
            </div>
          </div>

          <span className={`text-[11px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full border ${severityBadgeClass}`}>
            {advisory.severity} Stress
          </span>
        </div>

        {/* Hazard Title */}
        <div className="mb-3.5">
          <span className="text-xs font-semibold text-[#1F694B] uppercase tracking-wide block mb-1">
            Hazard Identified
          </span>
          <h4 className="text-sm sm:text-base font-bold text-[#1C231F]">
            {advisory.weather_hazard}
          </h4>
        </div>

        {/* Scientific Explanation */}
        <p className="text-xs sm:text-sm text-[#1C231F] leading-relaxed mb-4">
          {advisory.explanation}
        </p>

        {/* Possible Crop Consequence */}
        <div className="p-3.5 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1.5">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#B45309]">
            <AlertCircle className="w-3.5 h-3.5 shrink-0" />
            <span>Possible Crop Consequence</span>
          </div>
          <p className="text-xs text-[#1C231F] leading-relaxed">
            {advisory.possible_crop_consequence}
          </p>
        </div>
      </div>

      {/* Verified Citation Footer */}
      <div className="mt-5 pt-3 border-t border-[rgba(28,35,31,0.06)] flex items-center justify-between text-[11px] text-[#6B756F]">
        <div className="flex items-center gap-1">
          <BookOpen className="w-3 h-3 text-[#1F694B]" />
          <span>Citation:</span>
        </div>
        <span className="font-medium text-[#1C231F] truncate max-w-[200px]" title={advisory.source}>
          {advisory.source}
        </span>
      </div>
    </div>
  );
}

