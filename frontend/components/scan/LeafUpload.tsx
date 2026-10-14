'use client';

import React, { useState, useRef, useCallback } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertCircle, Sparkles, CheckCircle2, ShieldCheck, RefreshCw } from 'lucide-react';
import { predictLeafImage } from '@/lib/api';
import { PredictionResult } from '@/types';

interface LeafUploadProps {
  onPredictionComplete: (result: PredictionResult, imageSrc: string) => void;
  onAnalysisStart: () => void;
  onError: (errorMsg: string) => void;
}

// Curated high-yield real test samples for 1-click evaluation
const SAMPLE_LEAF_PRESETS = [
  {
    name: 'Tomato — Early Blight',
    crop: 'Tomato',
    description: 'Concentric target rings on leaf blade',
    url: 'https://images.unsplash.com/photo-1592417817098-8f3d69109853?auto=format&fit=crop&w=600&q=80',
  },
  {
    name: 'Apple — Healthy Leaf',
    crop: 'Apple',
    description: 'Uniform green surface, clear petiole',
    url: 'https://images.unsplash.com/photo-1590452366112-2591a27e7152?auto=format&fit=crop&w=600&q=80',
  },
  {
    name: 'Corn — Rust Infection',
    crop: 'Corn',
    description: 'Powdery rust pustules on upper blade',
    url: 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=600&q=80',
  },
];

export default function LeafUpload({ onPredictionComplete, onAnalysisStart, onError }: LeafUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [includeGradcam, setIncludeGradcam] = useState(true);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((file: File) => {
    // Validation: extensions
    const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      onError('Unsupported image format. Please upload a JPG, JPEG, PNG, or WEBP image.');
      return;
    }

    // Validation: size max 15MB
    if (file.size > 15 * 1024 * 1024) {
      onError('Image size exceeds 15MB. Please choose a smaller image.');
      return;
    }

    setSelectedFile(file);
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  }, [onError]);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleBrowse = () => {
    fileInputRef.current?.click();
  };

  const handleReset = () => {
    setSelectedFile(null);
    if (previewUrl && !previewUrl.startsWith('http')) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleAnalyze = async () => {
    if (!selectedFile && !previewUrl) {
      onError('Please select or upload a leaf image first.');
      return;
    }

    try {
      setIsAnalyzing(true);
      onAnalysisStart();

      let fileToUpload = selectedFile;
      if (!fileToUpload && previewUrl) {
        // If sample was chosen from remote URL, fetch blob
        const res = await fetch(previewUrl);
        const blob = await res.blob();
        fileToUpload = new File([blob], 'sample_leaf.jpg', { type: blob.type || 'image/jpeg' });
      }

      if (!fileToUpload) throw new Error('Could not prepare leaf image.');

      const result = await predictLeafImage(fileToUpload, includeGradcam);
      onPredictionComplete(result, previewUrl || '');
    } catch (err: any) {
      onError(err.message || 'Analysis failed. Please verify the backend is running and try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSampleClick = async (sampleUrl: string) => {
    setPreviewUrl(sampleUrl);
    setSelectedFile(null);
  };

  return (
    <div className="w-full space-y-6">
      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
      />

      {/* Main Bento Upload Card */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative w-full rounded-bento-xl border-2 transition-all p-8 sm:p-12 text-center bg-white shadow-bento ${
          isDragging
            ? 'border-[#1F694B] bg-[#E7F0EA]/40 scale-[1.008]'
            : 'border-dashed border-[rgba(28,35,31,0.15)] hover:border-[#1F694B]/50'
        }`}
      >
        {!previewUrl ? (
          /* Empty / Upload State */
          <div className="flex flex-col items-center justify-center max-w-lg mx-auto py-6">
            <div className="w-20 h-20 rounded-3xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] mb-6 shadow-sm group-hover:scale-105 transition-transform">
              <UploadCloud className="w-10 h-10 text-[#1F694B]" />
            </div>

            <h3 className="text-2xl font-bold text-[#1C231F] mb-2 tracking-tight">
              Upload or drag a plant leaf image
            </h3>
            <p className="text-sm text-[#6B756F] mb-8 leading-relaxed">
              For best accuracy, take a clear, well-lit photo of the affected leaf showing visible spots, discoloration, or healthy veins.
            </p>

            <div className="flex flex-col sm:flex-row items-center gap-4 w-full sm:w-auto">
              <button
                type="button"
                onClick={handleBrowse}
                className="w-full sm:w-auto px-8 py-3.5 rounded-full bg-[#1F694B] text-white text-base font-semibold shadow-sm hover:bg-[#18533b] hover:shadow-md transition-all active:scale-[0.98]"
              >
                Browse Image from Device
              </button>
            </div>

            <div className="mt-6 flex items-center gap-4 text-xs text-[#6B756F]">
              <span>JPG, JPEG, PNG, WEBP</span>
              <span>•</span>
              <span>Up to 15MB</span>
              <span>•</span>
              <span className="flex items-center gap-1 text-[#2E8B67] font-medium">
                <ShieldCheck className="w-3.5 h-3.5" /> No GenAI Hallucination
              </span>
            </div>
          </div>
        ) : (
          /* Selected Image Preview State */
          <div className="relative max-w-xl mx-auto flex flex-col items-center">
            {/* Reset button */}
            <button
              onClick={handleReset}
              disabled={isAnalyzing}
              className="absolute top-2 right-2 z-20 p-2.5 rounded-full bg-[#1C231F]/70 text-white hover:bg-[#1C231F] transition-all backdrop-blur-sm"
              title="Remove image"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Image Preview Container */}
            <div className="relative w-full aspect-square max-h-[380px] rounded-2xl overflow-hidden border border-[rgba(28,35,31,0.08)] bg-[#1C231F]/5 shadow-inner mb-6">
              <img
                src={previewUrl}
                alt="Selected leaf preview"
                className="w-full h-full object-contain"
              />

              {/* Scanning visual overlay when analyzing */}
              {isAnalyzing && (
                <div className="absolute inset-0 bg-[#1F694B]/15 backdrop-blur-[1px] flex flex-col items-center justify-center">
                  <div className="w-full h-1 bg-[#D6A434] absolute animate-scan shadow-[0_0_12px_#D6A434]" />
                  <div className="bg-white/95 px-6 py-3.5 rounded-2xl shadow-xl flex items-center gap-3 border border-[#1F694B]/20">
                    <RefreshCw className="w-5 h-5 text-[#1F694B] animate-spin" />
                    <div className="text-left">
                      <p className="text-sm font-bold text-[#1C231F]">Analyzing Leaf...</p>
                      <p className="text-xs text-[#6B756F]">EfficientNet-B0 evaluating 38 classes</p>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Options & Action */}
            <div className="w-full flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
              <label className="flex items-center gap-2.5 text-xs text-[#1C231F] cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={includeGradcam}
                  onChange={(e) => setIncludeGradcam(e.target.checked)}
                  disabled={isAnalyzing}
                  className="w-4 h-4 rounded text-[#1F694B] focus:ring-[#1F694B]"
                />
                <span className="font-medium">Generate Grad-CAM Attention Heatmap</span>
              </label>

              <div className="flex items-center gap-3 w-full sm:w-auto">
                <button
                  type="button"
                  onClick={handleReset}
                  disabled={isAnalyzing}
                  className="px-5 py-3 rounded-full border border-[rgba(28,35,31,0.15)] text-sm font-semibold text-[#1C231F] hover:bg-[#F7F5EE] transition-all"
                >
                  Change Photo
                </button>
                <button
                  type="button"
                  onClick={handleAnalyze}
                  disabled={isAnalyzing}
                  className="flex-1 sm:flex-none px-8 py-3 rounded-full bg-[#1F694B] text-white text-sm font-semibold shadow-sm hover:bg-[#18533b] hover:shadow-md transition-all active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin text-[#D6A434]" />
                      <span>Classifying...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-[#D6A434]" />
                      <span>Analyze Leaf</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 1-Click Test Presets Bento Strip */}
      {!previewUrl && (
        <div className="bg-white rounded-bento-lg p-6 border border-[rgba(28,35,31,0.08)] shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h4 className="text-sm font-bold text-[#1C231F] flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-[#D6A434]" />
                <span>Or Test Instantly with Sample Leaves</span>
              </h4>
              <p className="text-xs text-[#6B756F]">Click any sample image below to evaluate Model 1 without uploading your own file:</p>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {SAMPLE_LEAF_PRESETS.map((sample) => (
              <button
                key={sample.name}
                type="button"
                onClick={() => handleSampleClick(sample.url)}
                className="group text-left p-3 rounded-2xl border border-[rgba(28,35,31,0.06)] hover:border-[#1F694B] hover:bg-[#E7F0EA]/30 transition-all flex items-center gap-3.5"
              >
                <img
                  src={sample.url}
                  alt={sample.name}
                  className="w-14 h-14 rounded-xl object-cover border border-[rgba(28,35,31,0.08)] group-hover:scale-105 transition-transform"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-xs font-bold text-[#1C231F] truncate group-hover:text-[#1F694B] transition-colors">
                    {sample.name}
                  </p>
                  <p className="text-[11px] text-[#6B756F] truncate">{sample.description}</p>
                  <span className="text-[10px] text-[#2E8B67] font-semibold mt-1 inline-block">1-Click Test →</span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Privacy & Scope Disclaimer Card */}
      <div className="p-4 rounded-2xl bg-[#E7F0EA]/50 border border-[#2E8B67]/20 flex items-start gap-3 text-xs text-[#1C231F]">
        <CheckCircle2 className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
        <p className="leading-relaxed">
          <strong>AgroAI Privacy & Architecture:</strong> Your leaf photo is screened locally by Model 1 (EfficientNet-B0) across 38 PlantVillage classes. Disease guidance is drawn solely from verified agricultural extension facts — no generative AI language models are queried.
        </p>
      </div>
    </div>
  );
}

