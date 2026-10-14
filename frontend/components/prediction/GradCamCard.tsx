'use client';

import React, { useState } from 'react';
import { Eye, HelpCircle, Layers, Info } from 'lucide-react';

interface GradCamCardProps {
  gradcamImage?: string | null;
  originalImageSrc?: string;
  predictedDisease: string;
}

export default function GradCamCard({ gradcamImage, originalImageSrc, predictedDisease }: GradCamCardProps) {
  const [activeTab, setActiveTab] = useState<'side-by-side' | 'heatmap' | 'original'>('side-by-side');

  if (!gradcamImage) {
    return null;
  }

  return (
    <div className="bento-card p-6 overflow-hidden">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <Layers className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base text-[#1C231F]">Why the Model Predicted This (Grad-CAM)</h3>
          </div>
          <p className="text-xs text-[#6B756F] mt-1">
            Visual explanation of EfficientNet-B0 conv_head feature activations influencing &quot;{predictedDisease}&quot;.
          </p>
        </div>

        {/* Tab view controls */}
        <div className="flex items-center gap-1 bg-[#F7F5EE] p-1 rounded-xl self-start sm:self-auto border border-[rgba(28,35,31,0.06)]">
          <button
            type="button"
            onClick={() => setActiveTab('side-by-side')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'side-by-side' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F]'
            }`}
          >
            Side-by-Side
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('heatmap')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'heatmap' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F]'
            }`}
          >
            Heatmap Only
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('original')}
            className={`px-3 py-1 text-xs font-semibold rounded-lg transition-all ${
              activeTab === 'original' ? 'bg-white shadow-sm text-[#1F694B]' : 'text-[#6B756F]'
            }`}
          >
            Original
          </button>
        </div>
      </div>

      {/* Visual Display */}
      {activeTab === 'side-by-side' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold text-[#6B756F] uppercase tracking-wider">
              Input Leaf Image
            </span>
            <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)]">
              <img
                src={originalImageSrc || '/placeholder-leaf.jpg'}
                alt="Original leaf input"
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <span className="text-[11px] font-semibold text-[#1F694B] uppercase tracking-wider flex items-center justify-between">
              <span>Grad-CAM Activation Map</span>
              <span className="text-[10px] text-[#D6A434] font-bold">Warm = High Attention</span>
            </span>
            <div className="aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)]">
              <img
                src={gradcamImage}
                alt="Grad-CAM activation overlay"
                className="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'heatmap' && (
        <div className="max-w-md mx-auto aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)]">
          <img
            src={gradcamImage}
            alt="Grad-CAM activation overlay"
            className="w-full h-full object-cover"
          />
        </div>
      )}

      {activeTab === 'original' && (
        <div className="max-w-md mx-auto aspect-square rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)]">
          <img
            src={originalImageSrc || '/placeholder-leaf.jpg'}
            alt="Original leaf"
            className="w-full h-full object-cover"
          />
        </div>
      )}

      {/* Grad-CAM Disclaimer */}
      <div className="mt-5 p-3.5 rounded-xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] flex items-start gap-2.5 text-xs text-[#6B756F]">
        <Info className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>Explainability Notice:</strong> The reddish-yellow regions highlight the convolutional receptive fields that contributed most heavily to the model&apos;s decision. Grad-CAM is an interpretability visualization tool, not biological proof of disease.
        </p>
      </div>
    </div>
  );
}
