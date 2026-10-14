'use client';

import React from 'react';
import { Eye, CheckCircle2 } from 'lucide-react';

interface SymptomsCardProps {
  symptoms: string[];
}

export default function SymptomsCard({ symptoms }: SymptomsCardProps) {
  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
            <Eye className="w-4 h-4" />
          </div>
          <h3 className="font-bold text-base text-[#1C231F]">Identified Symptoms</h3>
        </div>

        <p className="text-xs text-[#6B756F] mb-4">
          Key visual markers documented by agricultural extension services:
        </p>

        {symptoms && symptoms.length > 0 ? (
          <ul className="space-y-3">
            {symptoms.map((symptom, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-[#1C231F] leading-relaxed">
                <span className="w-1.5 h-1.5 rounded-full bg-[#1F694B] mt-2 shrink-0" />
                <span>{symptom}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-[#6B756F] italic">No specific foliar symptoms reported.</p>
        )}
      </div>

      <div className="mt-6 pt-3 border-t border-[rgba(28,35,31,0.06)] text-[11px] text-[#6B756F]">
        Inspect both upper and lower leaf surfaces during scouting.
      </div>
    </div>
  );
}

