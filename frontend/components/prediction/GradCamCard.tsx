'use client';

import React, { useState } from 'react';
import { Eye, Layers, Info, Download, Sparkles, AlertCircle } from 'lucide-react';
import { GradCAMMetadata } from '@/types';

interface GradCamCardProps {
  gradcam?: GradCAMMetadata | null;
  gradcamImage?: string | null;
  originalImageSrc?: string;
  predictedDisease: string;
}

export default function GradCamCard({
  gradcam,
  gradcamImage,
  originalImageSrc,
  predictedDisease,
}: GradCamCardProps) {
  const [activeTab, setActiveTab] = useState<'side-by-side' | 'overlay' | 'heatmap' | 'original'>('side-by-side');

  // Resolve overlay & heatmap sources from metadata or fallback
  const overlaySrc = gradcam?.overlay_base64 || gradcamImage || (gradcam?.overlay_url ? `http://127.0.0.1:8000${gradcam.overlay_url}` : null);
  const heatmapSrc = gradcam?.heatmap_base64 || (gradcam?.heatmap_url ? `http://127.0.0.1:8000${gradcam.heatmap_url}` : overlaySrc);

  if (!overlaySrc && !gradcam?.available) {
    return null;
  }

  return (
    <div className="bento-card p-6 sm:p-8 overflow-hidden bg-white border border-[#2E8B67]/20 shadow-bento">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <Layers className="w-5 h-5 text-[#1F694B]" />
            </div>
            <div>
              <h3 className="font-bold text-lg text-[#1C231F] tracking-tight">
                Why the Model Predicted This (Grad-CAM)
              </h3>
              <p className="text-xs text-[#6B756F]">
                EfficientNetV2-S convolutional feature activations influencing &quot;{predictedDisease}&quot;.
              </p>
            </div>
          </div>
        </div>

        {/* 4-View Switcher */}
        <div className="flex items-center gap-1 bg-[#F7F5EE] p-1 rounded-xl self-start sm:self-auto border border-[rgba(28,35,31,0.06)]">
          <button
            type="button"
            onClick={() => setActiveTab('side-by-side')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'side-by-side' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F] hover:text-[#1C231F]'
            }`}
          >
            Side-by-Side
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('overlay')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'overlay' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F] hover:text-[#1C231F]'
            }`}
          >
            Overlay
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('heatmap')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'heatmap' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F] hover:text-[#1C231F]'
            }`}
          >
            Heatmap
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('original')}
            className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'original' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F] hover:text-[#1C231F]'
            }`}
          >
            Original
          </button>
        </div>
      </div>

      {/* Visual Display */}
      {activeTab === 'side-by-side' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] font-semibold text-[#6B756F] uppercase tracking-wider">
              <span>Input Leaf Image</span>
              <span>224×224 → 384×384</span>
            </div>
            <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-inner">
              <img
                src={originalImageSrc || '/placeholder-leaf.jpg'}
                alt="Original leaf input"
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-[11px] font-semibold text-[#1F694B] uppercase tracking-wider">
              <span>Grad-CAM Activation Map</span>
              <span className="text-[10px] text-[#D6A434] font-bold">Warm Colors = Diagnostic Focus</span>
            </div>
            <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-inner">
              <img
                src={overlaySrc || '/placeholder-leaf.jpg'}
                alt="Grad-CAM activation overlay"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'overlay' && (
        <div className="max-w-md mx-auto space-y-2">
          <span className="text-[11px] font-semibold text-[#1F694B] uppercase tracking-wider block text-center">
            Blended Feature Activation Overlay (Alpha 0.45)
          </span>
          <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-inner">
            <img
              src={overlaySrc || '/placeholder-leaf.jpg'}
              alt="Grad-CAM activation overlay"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      )}

      {activeTab === 'heatmap' && (
        <div className="max-w-md mx-auto space-y-2">
          <span className="text-[11px] font-semibold text-[#D6A434] uppercase tracking-wider block text-center">
            Raw JET Colormap Intensity
          </span>
          <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-inner">
            <img
              src={heatmapSrc || overlaySrc || '/placeholder-leaf.jpg'}
              alt="Raw Grad-CAM heatmap"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      )}

      {activeTab === 'original' && (
        <div className="max-w-md mx-auto space-y-2">
          <span className="text-[11px] font-semibold text-[#6B756F] uppercase tracking-wider block text-center">
            Original Unmodified Leaf
          </span>
          <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shadow-inner">
            <img
              src={originalImageSrc || '/placeholder-leaf.jpg'}
              alt="Original leaf"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      )}

      {/* Mandatory Disclaimer from PRD & Update Spec */}
      <div className="mt-6 p-4 rounded-2xl bg-[#E7F0EA]/60 border border-[#2E8B67]/20 flex items-start gap-3 text-xs text-[#1C231F]">
        <Info className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
        <div className="space-y-0.5">
          <p className="font-bold text-[#1F694B]">Explainability & Model Interpretation:</p>
          <p className="text-[#6B756F] leading-relaxed">
            Grad-CAM computes the gradient of the predicted class score with respect to feature maps in the final convolutional layer (<code className="bg-white/80 px-1 py-0.5 rounded text-[11px]">features.7</code>). Reddish-yellow areas indicate the leaf regions most strongly considered by the model. <strong>This is an AI visual explanation, not definitive biological proof of disease.</strong>
          </p>
        </div>
      </div>
    </div>
  );
}
