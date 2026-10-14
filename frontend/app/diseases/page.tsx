'use client';

import React from 'react';
import { BookOpen, ShieldCheck, Sparkles } from 'lucide-react';
import DiseaseBrowser from '@/components/knowledge/DiseaseBrowser';

export default function DiseasesPage() {
  return (
    <div className="w-full space-y-10 py-6 sm:py-10">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E7F0EA] border border-[#2E8B67]/20 text-xs font-semibold text-[#1F694B]">
          <BookOpen className="w-3.5 h-3.5 text-[#D6A434]" />
          <span>Verified Knowledge Base</span>
        </div>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-[#1C231F] tracking-tight">
          Supported Plant Diseases
        </h1>
        <p className="text-sm sm:text-base text-[#6B756F]">
          Explore symptoms, causal agents, agronomic prevention, and treatment protocols for all 38 classes supported by Model 1. Curated exclusively from university extension records.
        </p>
      </div>

      {/* Disease Explorer Grid */}
      <DiseaseBrowser />
    </div>
  );
}
