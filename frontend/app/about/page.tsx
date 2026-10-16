import React from 'react';
import Link from 'next/link';
import { Cpu, ShieldCheck, Database, Layers, ArrowRight, ExternalLink, CheckCircle2 } from 'lucide-react';

export default function AboutPage() {
  return (
    <div className="w-full max-w-4xl mx-auto py-8 sm:py-12 space-y-12">
      {/* Page Title */}
      <div className="text-center space-y-3">
        <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3.5 py-1.5 rounded-full border border-[#2E8B67]/20">
          Model Architecture &amp; Deployment Contract
        </span>
        <h1 className="text-3xl sm:text-5xl font-extrabold text-[#1C231F] tracking-tight">
          How AgroAI Works Under the Hood
        </h1>
        <p className="text-sm sm:text-base text-[#6B756F] max-w-2xl mx-auto">
          Complete disclosure on EfficientNetV2-S weights, metadata-driven deployment, integrated Grad-CAM explainability, and our strict No-GenAI policy.
        </p>
      </div>

      {/* Model Specifications Bento Grid */}
      <div className="bento-card p-8 bg-white space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-[#1C231F] flex items-center gap-2">
            <Cpu className="w-5 h-5 text-[#1F694B]" />
            <span>Active Model: EfficientNetV2-S + Grad-CAM</span>
          </h2>
          <span className="text-xs font-bold px-3 py-1 rounded-full bg-[#E7F0EA] text-[#1F694B]">
            Metadata Contract v1
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
          <div className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">99.58%</span>
            <span className="text-xs text-[#6B756F] block">Test Accuracy</span>
          </div>
          <div className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">99.36%</span>
            <span className="text-xs text-[#6B756F] block">Macro F1 Score</span>
          </div>
          <div className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">99.52%</span>
            <span className="text-xs text-[#6B756F] block">Validation F1</span>
          </div>
          <div className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">384×384</span>
            <span className="text-xs text-[#6B756F] block">Input Resolution</span>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-[#1C231F] pt-2">
          <div className="p-3.5 rounded-xl bg-[#F7F5EE] space-y-1">
            <span className="font-bold text-[#6B756F] uppercase tracking-wider block text-[10px]">Checkpoint &amp; Weights</span>
            <p className="font-mono font-medium truncate">efficientnetv2_s_38class_gradcam_best.pth</p>
          </div>
          <div className="p-3.5 rounded-xl bg-[#F7F5EE] space-y-1">
            <span className="font-bold text-[#6B756F] uppercase tracking-wider block text-[10px]">Grad-CAM Target Layer</span>
            <p className="font-mono font-medium">features.7 (Final conv activation block)</p>
          </div>
          <div className="p-3.5 rounded-xl bg-[#F7F5EE] space-y-1">
            <span className="font-bold text-[#6B756F] uppercase tracking-wider block text-[10px]">Deployment Contract</span>
            <p className="font-mono font-medium">efficientnetv2_s_metadata.json</p>
          </div>
          <div className="p-3.5 rounded-xl bg-[#F7F5EE] space-y-1">
            <span className="font-bold text-[#6B756F] uppercase tracking-wider block text-[10px]">Rollback Safety Strategy</span>
            <p className="font-mono font-medium">Archived EfficientNet-B0 (99.43% test acc) retained</p>
          </div>
        </div>
      </div>

      {/* Dataset Basis */}
      <div className="bento-card p-8 bg-white space-y-4">
        <h2 className="text-xl font-bold text-[#1C231F] flex items-center gap-2">
          <Database className="w-5 h-5 text-[#2E8B67]" />
          <span>Dataset Curation &amp; Audit</span>
        </h2>
        <p className="text-sm text-[#6B756F] leading-relaxed">
          The models are trained and validated using the clean PlantVillage agricultural color dataset:
        </p>
        <ul className="space-y-2 text-xs sm:text-sm text-[#1C231F]">
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
            <span><strong>54,305 original images</strong> were audited across 38 distinct classes.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
            <span><strong>21 exact duplicate images</strong> were detected and excised to prevent data leakage.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
            <span><strong>Zero corrupted files</strong> were found in the clean modeling dataframe (54,284 images).</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle2 className="w-4 h-4 text-[#1F694B] shrink-0 mt-0.5" />
            <span><strong>Stratified Split:</strong> ~80% Train (43,427), 10% Validation (5,428), 10% Test (5,429).</span>
          </li>
        </ul>
      </div>

      {/* Future-Proof Architecture */}
      <div className="bento-card p-8 bg-white space-y-4">
        <h2 className="text-xl font-bold text-[#1C231F] flex items-center gap-2">
          <Layers className="w-5 h-5 text-[#D6A434]" />
          <span>Decoupled Future-Proof Runtime Chain</span>
        </h2>
        <p className="text-sm text-[#6B756F] leading-relaxed">
          The Next.js frontend is decoupled from neural network internals via a standardized REST contract (<code className="bg-[#F7F5EE] px-1.5 py-0.5 rounded text-xs text-[#1F694B]">POST /api/v1/predict</code>). The backend dynamically constructs the vision pipeline directly from <code className="bg-[#F7F5EE] px-1.5 py-0.5 rounded text-xs text-[#1F694B]">efficientnetv2_s_metadata.json</code>:
        </p>

        {/* Runtime Flow Diagram */}
        <div className="p-5 rounded-2xl bg-[#1C231F] text-white font-mono text-xs overflow-x-auto leading-relaxed">
          <div className="text-[#D6A434]">metadata.json &rarr; Model Configuration (Size, Mean, Std, Target Layer)</div>
          <div className="text-[#2E8B67] pl-4">&darr; Construct EfficientNetV2-S</div>
          <div className="text-white pl-4">&rarr; Load .pth weights (efficientnetv2_s_38class_gradcam_best.pth)</div>
          <div className="text-[#A0A8A3] pl-4">&rarr; 38-class softmax prediction + Grad-CAM attention heatmap</div>
          <div className="text-[#2E8B67] pl-4">&darr; Query Verified Agricultural Knowledge Base (No GenAI)</div>
          <div className="text-white pl-4">&rarr; Next.js Bento Result Dashboard</div>
        </div>
      </div>

      {/* Strict No-GenAI Guarantee */}
      <div className="bento-card p-8 bg-[#E7F0EA]/70 border border-[#2E8B67]/30 space-y-3">
        <div className="flex items-center gap-2 text-[#1F694B]">
          <ShieldCheck className="w-6 h-6 text-[#1F694B]" />
          <h2 className="text-xl font-bold">Strict No-GenAI Policy</h2>
        </div>
        <p className="text-sm text-[#1C231F] leading-relaxed">
          AgroAI contains zero Generative AI. We do not query OpenAI, Gemini, Claude, or any LLM. Agricultural advice in our system is 100% deterministic, retrieved directly from a verified relational database seeded with official extension publications from USDA, UC IPM, Penn State, and Cornell University.
        </p>
      </div>

      {/* Return to Scan CTA */}
      <div className="text-center pt-4">
        <Link
          href="/scan"
          className="inline-flex items-center gap-2 px-8 py-3.5 rounded-full bg-[#1F694B] text-white text-sm font-semibold shadow-md hover:bg-[#18533b] transition-all"
        >
          <span>Try EfficientNetV2-S on a Leaf Image</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
