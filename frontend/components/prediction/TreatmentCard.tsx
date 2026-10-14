'use client';

import React from 'react';
import { Pill, AlertTriangle, ShieldCheck } from 'lucide-react';
import { TreatmentItem } from '@/types';

interface TreatmentCardProps {
  treatments: TreatmentItem[];
  safetyNotes?: string | null;
}

export default function TreatmentCard({ treatments, safetyNotes }: TreatmentCardProps) {
  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <Pill className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base text-[#1C231F]">Verified Treatment Options</h3>
          </div>
          <span className="text-[11px] font-semibold text-[#6B756F] bg-[#F7F5EE] px-2.5 py-0.5 rounded-full border border-[rgba(28,35,31,0.06)]">
            Verified Knowledge Only
          </span>
        </div>

        <p className="text-xs text-[#6B756F] mb-4">
          Actionable management protocols documented in university extension manuals:
        </p>

        {treatments && treatments.length > 0 ? (
          <div className="space-y-3.5">
            {treatments.map((tr, idx) => (
              <div key={idx} className="p-3.5 rounded-2xl bg-[#F7F5EE]/80 border border-[rgba(28,35,31,0.06)] space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#1F694B] px-2 py-0.5 rounded-md bg-white border border-[rgba(28,35,31,0.04)]">
                    {tr.treatment_type}
                  </span>
                </div>
                <p className="text-xs sm:text-sm text-[#1C231F] leading-relaxed">
                  {tr.description}
                </p>
                {tr.safety_note && (
                  <div className="flex items-start gap-1.5 text-[11px] text-[#B7791F] font-medium pt-1">
                    <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                    <span>Caution: {tr.safety_note}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-[#6B756F] italic">
            No specific chemical or therapeutic treatments required for this condition.
          </p>
        )}

        {/* Global Safety Note */}
        {safetyNotes && (
          <div className="mt-4 p-3.5 rounded-2xl bg-[#FFF7ED] border border-[#B7791F]/30 text-xs text-[#7C2D12] space-y-1">
            <div className="flex items-center gap-1.5 font-bold">
              <AlertTriangle className="w-3.5 h-3.5 text-[#B7791F]" />
              <span>Crop Safety & Harvest Advisory</span>
            </div>
            <p className="leading-relaxed">{safetyNotes}</p>
          </div>
        )}
      </div>

      <div className="mt-6 pt-3 border-t border-[rgba(28,35,31,0.06)] text-[11px] text-[#6B756F]">
        Follow local state pesticide regulations and observe pre-harvest intervals (PHI).
      </div>
    </div>
  );
}
