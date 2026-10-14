'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, BookOpen, ShieldCheck, Check, Pill, AlertTriangle, ExternalLink, RefreshCw, Scan } from 'lucide-react';
import { DiseaseDetail } from '@/types';
import { getDiseaseBySlug } from '@/lib/api';

export default function SingleDiseasePage() {
  const params = useParams();
  const router = useRouter();
  const slug = params?.slug as string;

  const [disease, setDisease] = useState<DiseaseDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;
    async function loadDetail() {
      try {
        setLoading(true);
        const data = await getDiseaseBySlug(slug);
        setDisease(data);
      } catch (err: any) {
        setError(err.message || 'Disease record not found.');
      } finally {
        setLoading(false);
      }
    }
    loadDetail();
  }, [slug]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-3">
        <RefreshCw className="w-8 h-8 text-[#1F694B] animate-spin" />
        <p className="text-sm text-[#6B756F]">Loading verified article...</p>
      </div>
    );
  }

  if (error || !disease) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <h2 className="text-2xl font-bold text-[#1C231F]">Disease Article Not Found</h2>
        <p className="text-sm text-[#6B756F]">{error || 'Could not find the requested agricultural record.'}</p>
        <Link
          href="/diseases"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#1F694B] text-white text-xs font-semibold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Diseases Library</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full max-w-5xl mx-auto py-8 sm:py-12 space-y-8">
      {/* Back link */}
      <div>
        <Link
          href="/diseases"
          className="inline-flex items-center gap-2 text-xs font-semibold text-[#1F694B] hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to All 38 Diseases</span>
        </Link>
      </div>

      {/* Hero Header Card */}
      <div className="bento-card p-8 sm:p-10 bg-white space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
            Crop: {disease.crop}
          </span>
          <span className="text-xs font-mono text-[#6B756F]">
            Raw Class: {disease.raw_class}
          </span>
        </div>

        <h1 className="text-3xl sm:text-5xl font-extrabold text-[#1C231F] tracking-tight">
          {disease.disease_name}
        </h1>

        {disease.causal_agent && (
          <p className="text-sm font-serif italic text-[#6B756F]">
            Pathogen: {disease.causal_agent}
          </p>
        )}

        <p className="text-base text-[#1C231F]/90 leading-relaxed pt-2">
          {disease.overview}
        </p>

        <div className="pt-4 border-t border-[rgba(28,35,31,0.06)] flex flex-wrap items-center justify-between gap-4">
          <div className="text-xs text-[#6B756F]">
            <strong>Verified Source:</strong> {disease.verified_source}
          </div>

          <Link
            href="/scan"
            className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#1F694B] text-white text-xs font-semibold shadow-sm hover:bg-[#18533b] transition-all"
          >
            <Scan className="w-4 h-4 text-[#D6A434]" />
            <span>Scan This Crop Now</span>
          </Link>
        </div>
      </div>

      {/* Bento Grid: Symptoms, Preventions & Treatments */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Symptoms */}
        <div className="bento-card p-6 bg-white space-y-3">
          <h3 className="font-bold text-base text-[#1C231F]">Documented Symptoms</h3>
          {disease.symptoms.length > 0 ? (
            <ul className="space-y-2.5 text-xs sm:text-sm text-[#1C231F]">
              {disease.symptoms.map((s, i) => (
                <li key={i} className="flex items-start gap-2.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#1F694B] mt-2 shrink-0" />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-[#6B756F]">No symptoms reported.</p>
          )}
        </div>

        {/* Prevention */}
        <div className="bento-card p-6 bg-white space-y-3">
          <h3 className="font-bold text-base text-[#1C231F]">Prevention & Cultural Management</h3>
          {disease.preventions.length > 0 ? (
            <ul className="space-y-2.5 text-xs sm:text-sm text-[#1C231F]">
              {disease.preventions.map((p, i) => (
                <li key={i} className="flex items-start gap-2.5">
                  <div className="w-4 h-4 rounded-full bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] mt-0.5 shrink-0">
                    <Check className="w-2.5 h-2.5 stroke-[3]" />
                  </div>
                  <span>{p}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-xs text-[#6B756F]">Standard cultural hygiene applies.</p>
          )}
        </div>
      </div>

      {/* Treatments Section */}
      <div className="bento-card p-8 bg-white space-y-4">
        <h3 className="font-bold text-lg text-[#1C231F]">Verified Management & Treatment Options</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {disease.treatments.map((t, i) => (
            <div key={i} className="p-4 rounded-2xl bg-[#F7F5EE] space-y-2 border border-[rgba(28,35,31,0.06)]">
              <span className="text-[10px] font-bold uppercase tracking-wider text-[#1F694B] px-2 py-0.5 rounded bg-white border border-[rgba(28,35,31,0.04)] inline-block">
                {t.treatment_type}
              </span>
              <p className="text-xs sm:text-sm text-[#1C231F] leading-relaxed">
                {t.description}
              </p>
              {t.safety_note && (
                <div className="flex items-start gap-1.5 text-[11px] text-[#B7791F] font-medium pt-1">
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                  <span>Caution: {t.safety_note}</span>
                </div>
              )}
            </div>
          ))}
        </div>

        {disease.safety_notes && (
          <div className="mt-4 p-4 rounded-2xl bg-[#FFF7ED] border border-[#B7791F]/30 text-xs text-[#7C2D12] space-y-1">
            <strong>Crop Safety Notice:</strong>
            <p>{disease.safety_notes}</p>
          </div>
        )}
      </div>

      {/* References */}
      {disease.references.length > 0 && (
        <div className="bento-card p-6 bg-white space-y-2 text-xs text-[#6B756F]">
          <h4 className="font-bold text-sm text-[#1C231F] mb-2">Extension Literature References</h4>
          <ul className="space-y-1">
            {disease.references.map((ref, i) => (
              <li key={i} className="flex items-center gap-2">
                <span>• {ref.title} ({ref.publisher})</span>
                {ref.url && (
                  <a href={ref.url} target="_blank" rel="noreferrer" className="text-[#1F694B] hover:underline flex items-center gap-1 font-medium">
                    <span>Link</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

