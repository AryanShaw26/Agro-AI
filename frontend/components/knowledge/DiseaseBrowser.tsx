'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Search, Filter, Leaf, ShieldAlert, CheckCircle2, ArrowRight, ExternalLink, RefreshCw } from 'lucide-react';
import { DiseaseListItem, DiseaseDetail } from '@/types';
import { getDiseases, getDiseaseBySlug } from '@/lib/api';

const CROPS = [
  'All Crops',
  'Apple',
  'Blueberry',
  'Cherry',
  'Corn (Maize)',
  'Grape',
  'Orange',
  'Peach',
  'Bell Pepper',
  'Potato',
  'Raspberry',
  'Soybean',
  'Squash',
  'Strawberry',
  'Tomato',
];

export default function DiseaseBrowser() {
  const [diseases, setDiseases] = useState<DiseaseListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('All Crops');
  const [selectedDiseaseDetail, setSelectedDiseaseDetail] = useState<DiseaseDetail | null>(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    async function loadData() {
      try {
        setLoading(true);
        const data = await getDiseases({
          crop: selectedCrop === 'All Crops' ? undefined : selectedCrop,
          search: search.trim() || undefined,
        });
        setDiseases(data);
      } catch (err) {
        console.error('Failed to load diseases:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [selectedCrop, search]);

  const handleOpenDetail = async (slug: string) => {
    try {
      setDetailLoading(true);
      const detail = await getDiseaseBySlug(slug);
      setSelectedDiseaseDetail(detail);
    } catch (err) {
      console.error('Failed to load detail:', err);
    } finally {
      setDetailLoading(false);
    }
  };

  return (
    <div className="w-full space-y-8">
      {/* Search & Filter Bento Bar */}
      <div className="bento-card p-6 bg-white">
        <div className="flex flex-col md:flex-row items-center gap-4">
          {/* Search Input */}
          <div className="relative w-full md:flex-1">
            <Search className="w-5 h-5 text-[#6B756F] absolute left-4 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search diseases, symptoms, or pathogens..."
              className="w-full pl-12 pr-4 py-3 rounded-xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] text-sm text-[#1C231F] focus:outline-none focus:ring-2 focus:ring-[#1F694B]"
            />
          </div>

          {/* Crop Selector */}
          <div className="w-full md:w-auto flex items-center gap-2 overflow-x-auto pb-2 md:pb-0">
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="px-4 py-3 rounded-xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] text-sm font-semibold text-[#1C231F] focus:outline-none focus:ring-2 focus:ring-[#1F694B] cursor-pointer"
            >
              {CROPS.map((crop) => (
                <option key={crop} value={crop}>
                  {crop}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Quick Filter Badges */}
        <div className="mt-4 flex flex-wrap gap-2 pt-2 border-t border-[rgba(28,35,31,0.06)]">
          {CROPS.slice(0, 8).map((crop) => (
            <button
              key={crop}
              type="button"
              onClick={() => setSelectedCrop(crop)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                selectedCrop === crop
                  ? 'bg-[#1F694B] text-white shadow-sm'
                  : 'bg-[#F7F5EE] text-[#6B756F] hover:bg-[#E7F0EA] hover:text-[#1F694B]'
              }`}
            >
              {crop}
            </button>
          ))}
        </div>
      </div>

      {/* Disease Cards Bento Grid */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <RefreshCw className="w-8 h-8 text-[#1F694B] animate-spin mb-3" />
          <p className="text-sm font-medium text-[#6B756F]">Loading verified agricultural articles...</p>
        </div>
      ) : diseases.length === 0 ? (
        <div className="bento-card p-12 text-center">
          <Leaf className="w-12 h-12 text-[#6B756F] mx-auto mb-3 opacity-40" />
          <h3 className="text-lg font-bold text-[#1C231F]">No matching plant conditions found</h3>
          <p className="text-xs text-[#6B756F] mt-1">Try refining your search terms or clearing the crop filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {diseases.map((d) => (
            <div
              key={d.id}
              onClick={() => handleOpenDetail(d.slug)}
              className="bento-card p-6 flex flex-col justify-between cursor-pointer hover:border-[#1F694B] group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-2.5 py-0.5 rounded-full">
                    {d.crop}
                  </span>
                  {d.is_healthy ? (
                    <span className="flex items-center gap-1 text-[11px] font-semibold text-[#2E8B67]">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Healthy State
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-[11px] font-semibold text-[#B7791F]">
                      <ShieldAlert className="w-3.5 h-3.5" /> Pathogen Condition
                    </span>
                  )}
                </div>

                <h3 className="font-bold text-lg text-[#1C231F] group-hover:text-[#1F694B] transition-colors mb-2">
                  {d.disease_name}
                </h3>

                <p className="text-xs text-[#6B756F] line-clamp-3 leading-relaxed mb-4">
                  {d.overview}
                </p>
              </div>

              <div className="pt-4 border-t border-[rgba(28,35,31,0.06)] flex items-center justify-between text-xs">
                <span className="text-[#6B756F] text-[11px] truncate max-w-[180px]">
                  {d.verified_source}
                </span>
                <span className="font-semibold text-[#1F694B] group-hover:translate-x-1 transition-transform inline-flex items-center gap-1">
                  Read Guide <ArrowRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Disease Detail Drawer / Modal */}
      {selectedDiseaseDetail && (
        <div className="fixed inset-0 z-50 bg-[#1C231F]/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-bento-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6 sm:p-8 shadow-2xl space-y-6">
            <div className="flex items-start justify-between border-b border-[rgba(28,35,31,0.08)] pb-4">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-2.5 py-1 rounded-full">
                  {selectedDiseaseDetail.crop}
                </span>
                <h2 className="text-2xl font-extrabold text-[#1C231F] mt-2">
                  {selectedDiseaseDetail.disease_name}
                </h2>
                {selectedDiseaseDetail.causal_agent && (
                  <p className="text-xs text-[#6B756F] italic mt-0.5">
                    Pathogen: {selectedDiseaseDetail.causal_agent}
                  </p>
                )}
              </div>
              <button
                type="button"
                onClick={() => setSelectedDiseaseDetail(null)}
                className="p-2 rounded-full hover:bg-[#F7F5EE] text-[#6B756F] text-sm font-bold"
              >
                ✕
              </button>
            </div>

            {/* Overview */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-[#6B756F] mb-1">
                Verified Overview
              </h4>
              <p className="text-sm text-[#1C231F] leading-relaxed">
                {selectedDiseaseDetail.overview}
              </p>
            </div>

            {/* Symptoms */}
            {selectedDiseaseDetail.symptoms.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#6B756F] mb-2">
                  Key Symptoms
                </h4>
                <ul className="space-y-1.5 text-xs text-[#1C231F]">
                  {selectedDiseaseDetail.symptoms.map((s, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#1F694B] mt-1.5 shrink-0" />
                      <span>{s}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Prevention */}
            {selectedDiseaseDetail.preventions.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#6B756F] mb-2">
                  Prevention & Cultural Management
                </h4>
                <ul className="space-y-1.5 text-xs text-[#1C231F]">
                  {selectedDiseaseDetail.preventions.map((p, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-[#2E8B67] mt-1.5 shrink-0" />
                      <span>{p}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Treatments */}
            {selectedDiseaseDetail.treatments.length > 0 && (
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#6B756F] mb-2">
                  Verified Treatments
                </h4>
                <div className="space-y-2">
                  {selectedDiseaseDetail.treatments.map((t, i) => (
                    <div key={i} className="p-3 rounded-xl bg-[#F7F5EE] text-xs space-y-1">
                      <span className="font-bold text-[#1F694B] uppercase tracking-wider text-[10px] block">
                        [{t.treatment_type}]
                      </span>
                      <p className="text-[#1C231F]">{t.description}</p>
                      {t.safety_note && (
                        <p className="text-[#B7791F] font-medium text-[11px]">
                          Caution: {t.safety_note}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-4 border-t border-[rgba(28,35,31,0.08)] flex justify-between items-center text-xs text-[#6B756F]">
              <span>Source: {selectedDiseaseDetail.verified_source}</span>
              <button
                type="button"
                onClick={() => setSelectedDiseaseDetail(null)}
                className="px-5 py-2 rounded-full bg-[#1F694B] text-white font-semibold text-xs"
              >
                Close Guide
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
