'use client';

import React from 'react';
import { CheckCircle, AlertTriangle, ShieldAlert, Sparkles, Download, ArrowLeft, RefreshCw, FileText } from 'lucide-react';
import Link from 'next/link';
import { PredictionResult } from '@/types';
import { getReportPdfUrl } from '@/lib/api';

interface PredictionHeroProps {
  result: PredictionResult;
  originalImageSrc?: string;
  onReset: () => void;
}

export default function PredictionHero({ result, originalImageSrc, onReset }: PredictionHeroProps) {
  const isHealthy = result.is_healthy;
  const isUncertain = result.confidence_state === 'uncertain';
  const confidencePercent = (result.confidence * 100).toFixed(1);

  return (
    <div className="w-full space-y-6">
      {/* Uncertain / Low Confidence Advisory Banner (if applicable) */}
      {isUncertain && (
        <div className="p-4 sm:p-5 rounded-bento-md bg-[#FFF7ED] border border-[#B7791F]/30 flex items-start gap-3.5 shadow-sm">
          <ShieldAlert className="w-5 h-5 text-[#B7791F] shrink-0 mt-0.5" />
          <div className="text-xs sm:text-sm text-[#7C2D12] space-y-1">
            <p className="font-bold">Low Model Confidence Advisory (&lt; 70% threshold)</p>
            <p className="leading-relaxed">
              The model detected visual ambiguity in this leaf sample. The predicted condition is shown for screening orientation, but we strongly recommend manual inspection by a local agronomic extension specialist before initiating chemical treatments.
            </p>
          </div>
        </div>
      )}

      {/* Main 2x2 Bento Hero Card */}
      <div className={`bento-card p-6 sm:p-8 overflow-hidden relative ${
        isHealthy 
          ? 'border-[#2E8B67]/30 bg-gradient-to-br from-white via-white to-[#E7F0EA]/50'
          : isUncertain
          ? 'border-[#B7791F]/30 bg-gradient-to-br from-white via-white to-[#FFF7ED]/40'
          : 'border-[rgba(28,35,31,0.08)] bg-white'
      }`}>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          {/* Leaf Visual / Scan Preview */}
          <div className="lg:col-span-5 relative">
            <div className="relative w-full aspect-square max-h-[320px] rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-sm">
              <img
                src={originalImageSrc || result.image_preview_url || '/placeholder-leaf.jpg'}
                alt={result.disease}
                className="w-full h-full object-cover"
              />
              {/* Status pill over image */}
              <div className="absolute top-3 left-3">
                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold backdrop-blur-md shadow-sm ${
                  isHealthy
                    ? 'bg-[#1F694B] text-white'
                    : isUncertain
                    ? 'bg-[#B7791F] text-white'
                    : 'bg-[#1C231F]/80 text-white'
                }`}>
                  {isHealthy ? (
                    <>
                      <CheckCircle className="w-3.5 h-3.5 text-[#E7F0EA]" /> Healthy Tissue
                    </>
                  ) : (
                    <>
                      <AlertTriangle className="w-3.5 h-3.5 text-[#D6A434]" /> Foliar Disease Detected
                    </>
                  )}
                </span>
              </div>
            </div>
          </div>

          {/* Diagnostic Details */}
          <div className="lg:col-span-7 space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
                Crop: {result.crop}
              </span>
              <span className="text-xs text-[#6B756F]">
                Inference: {result.processing_time_ms} ms
              </span>
            </div>

            <div>
              <h1 className="text-3xl sm:text-4xl font-extrabold text-[#1C231F] tracking-tight leading-tight">
                {result.disease}
              </h1>
              {result.knowledge.causal_agent && (
                <p className="text-xs sm:text-sm text-[#6B756F] italic mt-1 font-serif">
                  Pathogen: {result.knowledge.causal_agent}
                </p>
              )}
            </div>

            {/* Confidence indicator row */}
            <div className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] flex items-center justify-between">
              <div>
                <p className="text-xs font-semibold text-[#6B756F] uppercase tracking-wider">
                  Model Confidence
                </p>
                <div className="flex items-baseline gap-2 mt-0.5">
                  <span className="text-3xl font-extrabold text-[#1F694B]">
                    {confidencePercent}%
                  </span>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded-md ${
                    isUncertain
                      ? 'bg-[#B7791F]/10 text-[#B7791F]'
                      : 'bg-[#1F694B]/10 text-[#1F694B]'
                  }`}>
                    {result.confidence_state.toUpperCase()}
                  </span>
                </div>
              </div>

              <div className="text-right">
                <span className="text-xs text-[#6B756F] block">Model Checkpoint</span>
                <span className="text-xs font-mono font-medium text-[#1C231F]">
                  {result.model_version}
                </span>
              </div>
            </div>

            {/* Quick overview excerpt */}
            <p className="text-sm text-[#1C231F]/80 leading-relaxed">
              {result.knowledge.overview || 'Verified agricultural overview is loaded from extension records below.'}
            </p>

            {/* Action buttons */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <a
                href={getReportPdfUrl(result.prediction_id)}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1F694B] text-white text-xs sm:text-sm font-semibold shadow-sm hover:bg-[#18533b] transition-all"
              >
                <Download className="w-4 h-4 text-[#D6A434]" />
                <span>Download PDF Report</span>
              </a>

              <button
                type="button"
                onClick={onReset}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full border border-[rgba(28,35,31,0.15)] bg-white text-xs sm:text-sm font-semibold text-[#1C231F] hover:bg-[#F7F5EE] transition-all"
              >
                <RefreshCw className="w-4 h-4 text-[#6B756F]" />
                <span>New Scan</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
