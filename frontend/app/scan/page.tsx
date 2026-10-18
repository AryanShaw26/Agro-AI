'use client';

import React, { useState } from 'react';
import { Scan, Sparkles, AlertCircle, ArrowLeft, RefreshCw } from 'lucide-react';
import LeafUpload from '@/components/scan/LeafUpload';
import PredictionHero from '@/components/prediction/PredictionHero';
import TopPredictions from '@/components/prediction/TopPredictions';
import KnowledgeCard from '@/components/prediction/KnowledgeCard';
import SymptomsCard from '@/components/prediction/SymptomsCard';
import PreventionCard from '@/components/prediction/PreventionCard';
import TreatmentCard from '@/components/prediction/TreatmentCard';
import GradCamCard from '@/components/prediction/GradCamCard';
import WeatherSection from '@/components/weather/WeatherSection';
import { PredictionResult } from '@/types';

export default function ScanPage() {
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [originalImageSrc, setOriginalImageSrc] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handlePredictionComplete = (result: PredictionResult, imageSrc: string) => {
    setPrediction(result);
    setOriginalImageSrc(imageSrc);
    setIsAnalyzing(false);
    setErrorMessage(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleAnalysisStart = () => {
    setIsAnalyzing(true);
    setErrorMessage(null);
  };

  const handleError = (errorMsg: string) => {
    setErrorMessage(errorMsg);
    setIsAnalyzing(false);
  };

  const handleReset = () => {
    setPrediction(null);
    setOriginalImageSrc('');
    setErrorMessage(null);
    setIsAnalyzing(false);
  };

  return (
    <div className="w-full space-y-10 py-6 sm:py-10">
      {/* Page Title & Context Header */}
      {!prediction && (
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E7F0EA] border border-[#2E8B67]/20 text-xs font-semibold text-[#1F694B]">
            <Scan className="w-3.5 h-3.5 text-[#D6A434]" />
            <span>AI Diagnostic Screening</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-[#1C231F] tracking-tight">
            What&apos;s happening to your plant?
          </h1>
          <p className="text-sm sm:text-base text-[#6B756F]">
            Upload a clear photo of the symptomatic leaf. EfficientNet-B0 analyzes the image across 38 crop classes in real-time.
          </p>
        </div>
      )}

      {/* Error message banner */}
      {errorMessage && (
        <div className="max-w-2xl mx-auto p-4 rounded-2xl bg-red-50 border border-[#B84A4A]/20 flex items-start gap-3 text-xs sm:text-sm text-[#B84A4A]">
          <AlertCircle className="w-5 h-5 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-bold">Screening Error</p>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}

      {/* Primary Content: Upload vs Result Bento Dashboard */}
      {!prediction ? (
        <div className="space-y-10">
          <div className="max-w-3xl mx-auto">
            <LeafUpload
              onPredictionComplete={handlePredictionComplete}
              onAnalysisStart={handleAnalysisStart}
              onError={handleError}
            />
          </div>

          {/* Pre-scan Ambient Environmental Context */}
          <div className="max-w-5xl mx-auto pt-6 border-t border-[rgba(28,35,31,0.06)]">
            <WeatherSection
              customBannerText="Current ambient environmental conditions around you. Review local microclimate factors before screening."
              showTitle={true}
            />
          </div>
        </div>
      ) : (
        /* Bento Result Dashboard (PRD Section 17 & 18) */
        <div className="w-full space-y-8 animate-fadeIn">
          {/* Navigation & Reset Strip */}
          <div className="flex items-center justify-between">
            <button
              type="button"
              onClick={handleReset}
              className="inline-flex items-center gap-2 text-xs font-semibold text-[#1F694B] hover:underline"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Upload</span>
            </button>

            <span className="text-xs text-[#6B756F]">
              Scan ID: <span className="font-mono">{prediction.prediction_id.slice(0, 8)}</span>
            </span>
          </div>

          {/* 1. Prediction Hero Card (2x2 unit) */}
          <PredictionHero
            result={prediction}
            originalImageSrc={originalImageSrc}
            onReset={handleReset}
          />

          {/* 2. Top-3 Predictions & Overview Bento Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-5">
              <TopPredictions topPredictions={prediction.top_predictions} />
            </div>
            <div className="lg:col-span-7">
              <KnowledgeCard
                knowledge={prediction.knowledge}
                diseaseName={prediction.disease}
              />
            </div>
          </div>

          {/* 3. First-Class Grad-CAM Visual Heatmap Card */}
          {(prediction.gradcam?.available || prediction.gradcam_image) && (
            <GradCamCard
              gradcam={prediction.gradcam}
              gradcamImage={prediction.gradcam_image}
              originalImageSrc={originalImageSrc}
              predictedDisease={prediction.disease}
            />
          )}

          {/* 4. Symptoms, Prevention & Treatment Bento Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <SymptomsCard symptoms={prediction.knowledge.symptoms} />
            <PreventionCard preventions={prediction.knowledge.preventions} />
            <TreatmentCard
              treatments={prediction.knowledge.treatments}
              safetyNotes={prediction.knowledge.safety_notes}
            />
          </div>

          {/* 5. Environmental Weather Intelligence (Independent Advisory Layer) */}
          <WeatherSection />
        </div>
      )}
    </div>
  );
}

