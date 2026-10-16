'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { useParams, useRouter } from 'next/navigation';
import { ArrowLeft, RefreshCw, AlertCircle, Scan } from 'lucide-react';
import { PredictionResult } from '@/types';
import { getPredictionById } from '@/lib/api';
import PredictionHero from '@/components/prediction/PredictionHero';
import TopPredictions from '@/components/prediction/TopPredictions';
import KnowledgeCard from '@/components/prediction/KnowledgeCard';
import SymptomsCard from '@/components/prediction/SymptomsCard';
import PreventionCard from '@/components/prediction/PreventionCard';
import TreatmentCard from '@/components/prediction/TreatmentCard';
import GradCamCard from '@/components/prediction/GradCamCard';

export default function PredictionResultPage() {
  const params = useParams();
  const router = useRouter();
  const predictionId = params?.predictionId as string;

  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!predictionId) return;
    async function loadResult() {
      try {
        setLoading(true);
        const data = await getPredictionById(predictionId);
        setResult(data);
      } catch (err: any) {
        setError(err.message || 'Prediction not found');
      } finally {
        setLoading(false);
      }
    }
    loadResult();
  }, [predictionId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-24 space-y-3">
        <RefreshCw className="w-8 h-8 text-[#1F694B] animate-spin" />
        <p className="text-sm text-[#6B756F]">Retrieving diagnostic scan record...</p>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <h2 className="text-2xl font-bold text-[#1C231F]">Scan Record Not Found</h2>
        <p className="text-sm text-[#6B756F]">{error || 'Could not locate the requested prediction ID.'}</p>
        <Link
          href="/scan"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#1F694B] text-white text-xs font-semibold"
        >
          <Scan className="w-4 h-4 text-[#D6A434]" />
          <span>Launch New Scan</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full space-y-8 py-8 animate-fadeIn">
      {/* Navigation */}
      <div className="flex items-center justify-between">
        <Link
          href="/scan"
          className="inline-flex items-center gap-2 text-xs font-semibold text-[#1F694B] hover:underline"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Scan Another Leaf</span>
        </Link>

        <span className="text-xs text-[#6B756F]">
          Scan ID: <span className="font-mono">{result.prediction_id.slice(0, 8)}</span>
        </span>
      </div>

      {/* 1. Prediction Hero */}
      <PredictionHero
        result={result}
        originalImageSrc={result.image_preview_url || undefined}
        onReset={() => router.push('/scan')}
      />

      {/* 2. Top-3 Predictions & Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-5">
          <TopPredictions topPredictions={result.top_predictions} />
        </div>
        <div className="lg:col-span-7">
          <KnowledgeCard
            knowledge={result.knowledge}
            diseaseName={result.disease}
          />
        </div>
      </div>

      {/* 3. Grad-CAM Attention Heatmap Card */}
      {(result.gradcam?.available || result.gradcam_image) && (
        <GradCamCard
          gradcam={result.gradcam}
          gradcamImage={result.gradcam_image}
          originalImageSrc={result.image_preview_url || undefined}
          predictedDisease={result.disease}
        />
      )}

      {/* 4. Symptoms, Prevention & Treatments */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <SymptomsCard symptoms={result.knowledge.symptoms} />
        <PreventionCard preventions={result.knowledge.preventions} />
        <TreatmentCard
          treatments={result.knowledge.treatments}
          safetyNotes={result.knowledge.safety_notes}
        />
      </div>
    </div>
  );
}

