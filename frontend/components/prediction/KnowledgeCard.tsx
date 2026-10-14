'use client';

import React from 'react';
import { BookOpen, ShieldCheck, AlertCircle, Info, ExternalLink } from 'lucide-react';
import { KnowledgeData } from '@/types';

interface KnowledgeCardProps {
  knowledge: KnowledgeData;
  diseaseName: string;
}

export default function KnowledgeCard({ knowledge, diseaseName }: KnowledgeCardProps) {
  if (!knowledge.available) {
    return (
      <div className="bento-card p-6 border-dashed border-[#B7791F]/30 bg-[#FFF7ED]/30">
        <div className="flex items-center gap-2 mb-2 text-[#B7791F]">
          <AlertCircle className="w-5 h-5" />
          <h3 className="font-bold text-sm">Verified Guidance Unavailable</h3>
        </div>
        <p className="text-xs text-[#6B756F]">
          No verified agricultural article has been mapped to this condition yet. AgroAI does not invent or hallucinate agricultural facts.
        </p>
      </div>
    );
  }

  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <BookOpen className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base text-[#1C231F]">Verified Disease Overview</h3>
          </div>
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-[#1F694B] bg-[#E7F0EA] px-2.5 py-1 rounded-full">
            <ShieldCheck className="w-3.5 h-3.5" /> Peer Verified
          </span>
        </div>

        <p className="text-sm text-[#1C231F]/85 leading-relaxed mb-6">
          {knowledge.overview}
        </p>

        {/* Pathogen & Severity badges */}
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div className="p-3 rounded-xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)]">
            <span className="text-[11px] text-[#6B756F] uppercase tracking-wider block font-semibold">Causal Agent</span>
            <span className="text-xs font-bold text-[#1C231F] italic block truncate">
              {knowledge.causal_agent || 'Foliar condition'}
            </span>
          </div>

          <div className="p-3 rounded-xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)]">
            <span className="text-[11px] text-[#6B756F] uppercase tracking-wider block font-semibold">Severity</span>
            <span className="text-xs font-bold text-[#1C231F] block truncate">
              {knowledge.severity || 'Field monitoring'}
            </span>
          </div>
        </div>
      </div>

      {/* Source Citation */}
      <div className="pt-4 border-t border-[rgba(28,35,31,0.06)] flex items-center justify-between text-xs text-[#6B756F]">
        <span className="truncate">Source: {knowledge.verified_source}</span>
        {knowledge.references?.[0]?.url && (
          <a
            href={knowledge.references[0].url}
            target="_blank"
            rel="noreferrer"
            className="text-[#1F694B] hover:underline flex items-center gap-1 shrink-0 font-medium ml-2"
          >
            <span>Reference</span>
            <ExternalLink className="w-3 h-3" />
          </a>
        )}
      </div>
    </div>
  );
}

