'use client';

import React from 'react';
import { ShieldAlert, CheckCircle2, Info, AlertTriangle } from 'lucide-react';
import { WeatherAdvisory } from '@/types/weather';

interface WeatherProtectionCardProps {
  advisory?: WeatherAdvisory | null;
  loading?: boolean;
}

export default function WeatherProtectionCard({ advisory, loading }: WeatherProtectionCardProps) {
  if (loading && !advisory) {
    return (
      <div className="bento-card p-6 h-full flex flex-col justify-center items-center text-[#6B756F] space-y-2">
        <ShieldAlert className="w-6 h-6 animate-pulse text-[#1F694B]" />
        <span className="text-xs">Formulating environmental protection advisory...</span>
      </div>
    );
  }

  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-base text-[#1C231F]">Weather Protection / What You Can Do</h3>
              <p className="text-[11px] text-[#6B756F]">Environmental risk mitigations</p>
            </div>
          </div>

          <span className="text-[11px] font-semibold text-[#1F694B] bg-[#E7F0EA] px-2.5 py-0.5 rounded-full border border-[rgba(28,35,31,0.06)]">
            Action Checklist
          </span>
        </div>

        <p className="text-xs text-[#6B756F] mb-4">
          Agronomic field management steps to minimize crop damage from ambient weather conditions:
        </p>

        {/* Actions List */}
        {advisory?.actions && advisory.actions.length > 0 ? (
          <div className="space-y-3 mb-5">
            {advisory.actions.map((act, idx) => (
              <div key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-[#1C231F] leading-relaxed">
                <div className="w-4 h-4 rounded-full bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] mt-0.5 shrink-0">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                </div>
                <span>{act}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-[#6B756F] italic mb-5">
            Standard agronomic practices and regular scouting are recommended under current weather conditions.
          </p>
        )}

        {/* Environmental Boundary Disclaimer */}
        <div className="p-3.5 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#6B756F]">
            <Info className="w-3.5 h-3.5 text-[#1F694B] shrink-0" />
            <span>Environmental Boundary Context</span>
          </div>
          <p className="text-[11px] text-[#6B756F] leading-relaxed">
            {advisory?.limitations ||
              'Environmental advisory only. Weather conditions describe ambient field surroundings and do not diagnose plant disease or override leaf laboratory tests.'}
          </p>
        </div>
      </div>

      <div className="mt-5 pt-3 border-t border-[rgba(28,35,31,0.06)] text-[11px] text-[#1F694B] font-medium flex items-center gap-1.5">
        <AlertTriangle className="w-3.5 h-3.5 text-[#D6A434]" />
        <span>Independent from leaf vision diagnosis</span>
      </div>
    </div>
  );
}

