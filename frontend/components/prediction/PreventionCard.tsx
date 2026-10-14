'use client';

import React from 'react';
import { Shield, Check } from 'lucide-react';

interface PreventionCardProps {
  preventions: string[];
}

export default function PreventionCard({ preventions }: PreventionCardProps) {
  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
            <Shield className="w-4 h-4" />
          </div>
          <h3 className="font-bold text-base text-[#1C231F]">Prevention & Cultural Care</h3>
        </div>

        <p className="text-xs text-[#6B756F] mb-4">
          Agronomic guidelines to inhibit disease entry and canopy spread:
        </p>

        {preventions && preventions.length > 0 ? (
          <ul className="space-y-3">
            {preventions.map((prev, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs sm:text-sm text-[#1C231F] leading-relaxed">
                <div className="w-4 h-4 rounded-full bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] mt-0.5 shrink-0">
                  <Check className="w-2.5 h-2.5 stroke-[3]" />
                </div>
                <span>{prev}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-xs text-[#6B756F] italic">Follow standard crop hygiene and good agricultural practices.</p>
        )}
      </div>

      <div className="mt-6 pt-3 border-t border-[rgba(28,35,31,0.06)] text-[11px] text-[#2E8B67] font-medium">
        Pre-infection prevention delivers highest crop protection.
      </div>
    </div>
  );
}
