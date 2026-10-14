'use client';

import React from 'react';
import Link from 'next/link';
import {
  Scan,
  ShieldCheck,
  CheckCircle2,
  Cpu,
  Layers,
  FileText,
  ArrowRight,
  BookOpen,
  Sparkles,
  HelpCircle,
  ExternalLink,
  ChevronDown
} from 'lucide-react';

export default function HomePage() {
  return (
    <div className="w-full space-y-20 pb-16">
      {/* 1. HERO SECTION — Asymmetric Bento Hero */}
      <section className="pt-8 sm:pt-14">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
          {/* Left Large Bento Block (7 cols) */}
          <div className="lg:col-span-7 bento-card p-8 sm:p-12 flex flex-col justify-between bg-white relative overflow-hidden">
            <div className="space-y-6 relative z-10">
              {/* Eyebrow badge */}
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#E7F0EA] border border-[#2E8B67]/20 text-xs font-semibold text-[#1F694B]">
                <Sparkles className="w-3.5 h-3.5 text-[#D6A434]" />
                <span>Model 1: EfficientNet-B0 Plant Disease Classifier</span>
              </div>

              {/* Display Headline */}
              <h1 className="text-4xl sm:text-6xl font-extrabold text-[#1C231F] tracking-tight leading-[1.08]">
                Scan. <br />
                <span className="text-[#1F694B]">Understand.</span> <br />
                Protect.
              </h1>

              {/* Supporting Copy */}
              <p className="text-base sm:text-lg text-[#6B756F] leading-relaxed max-w-xl">
                Upload a plant-leaf image and let AgroAI identify the most likely disease across 38 crop conditions. Backed by verified agricultural science — strictly without Generative AI hallucinations.
              </p>
            </div>

            {/* CTAs & Micro-trust */}
            <div className="mt-10 pt-6 border-t border-[rgba(28,35,31,0.06)] space-y-4 relative z-10">
              <div className="flex flex-col sm:flex-row items-center gap-4">
                <Link
                  href="/scan"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-8 py-4 rounded-full bg-[#1F694B] text-white text-base font-semibold shadow-md hover:bg-[#18533b] hover:shadow-lg transition-all active:scale-[0.98]"
                >
                  <Scan className="w-5 h-5 text-[#D6A434]" />
                  <span>Scan a Leaf Now</span>
                  <ArrowRight className="w-4 h-4" />
                </Link>

                <Link
                  href="/diseases"
                  className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-4 rounded-full border border-[rgba(28,35,31,0.15)] bg-white text-sm font-semibold text-[#1C231F] hover:bg-[#F7F5EE] transition-all"
                >
                  <BookOpen className="w-4 h-4 text-[#1F694B]" />
                  <span>Explore 38 Classes</span>
                </Link>
              </div>

              <div className="flex items-center gap-6 text-xs text-[#6B756F] pt-2">
                <span className="flex items-center gap-1.5 text-[#1F694B] font-medium">
                  <CheckCircle2 className="w-4 h-4 text-[#2E8B67]" /> 99.43% Test Accuracy
                </span>
                <span>•</span>
                <span className="flex items-center gap-1.5 text-[#1F694B] font-medium">
                  <ShieldCheck className="w-4 h-4 text-[#2E8B67]" /> Verified Knowledge Only
                </span>
              </div>
            </div>

            {/* Subtle background botanical ambient */}
            <div className="absolute -bottom-16 -right-16 w-64 h-64 bg-[#E7F0EA]/70 rounded-full blur-3xl pointer-events-none" />
          </div>

          {/* Right Bento Visual Diagnostic Card (5 cols) */}
          <div className="lg:col-span-5 bento-card p-6 sm:p-8 bg-gradient-to-br from-[#1C231F] to-[#25302A] text-white flex flex-col justify-between relative overflow-hidden">
            {/* Visual Header */}
            <div className="flex items-center justify-between z-10">
              <span className="text-xs uppercase tracking-wider font-semibold text-[#D6A434]">
                Diagnostic Scanner
              </span>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/10 text-white/80">
                Model v1.0
              </span>
            </div>

            {/* Simulated Leaf Scan with Brackets */}
            <div className="my-6 relative z-10">
              <div className="relative aspect-square max-h-[260px] mx-auto rounded-2xl overflow-hidden border border-white/20 shadow-2xl">
                <img
                  src="https://images.unsplash.com/photo-1592417817098-8f3d69109853?auto=format&fit=crop&w=600&q=80"
                  alt="Scanning leaf sample"
                  className="w-full h-full object-cover"
                />

                {/* Diagnostic scan overlay brackets */}
                <div className="absolute inset-4 border-2 border-[#2E8B67]/70 rounded-xl pointer-events-none">
                  <div className="absolute -top-1 -left-1 w-4 h-4 border-t-2 border-l-2 border-[#D6A434]" />
                  <div className="absolute -top-1 -right-1 w-4 h-4 border-t-2 border-r-2 border-[#D6A434]" />
                  <div className="absolute -bottom-1 -left-1 w-4 h-4 border-b-2 border-l-2 border-[#D6A434]" />
                  <div className="absolute -bottom-1 -right-1 w-4 h-4 border-b-2 border-r-2 border-[#D6A434]" />
                </div>

                {/* Floating Prediction Preview Badge */}
                <div className="absolute bottom-3 left-3 right-3 bg-[#1C231F]/90 backdrop-blur-md p-3 rounded-xl border border-white/10 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-[#F7F5EE]">Tomato — Early Blight</span>
                    <span className="text-[#D6A434] font-bold">99.4% confidence</span>
                  </div>
                  <p className="text-[10px] text-[#A0A8A3] truncate">
                    Alternaria linariae • Concentric target lesions
                  </p>
                </div>
              </div>
            </div>

            {/* Quick telemetry metrics */}
            <div className="grid grid-cols-3 gap-2 pt-4 border-t border-white/10 z-10 text-center">
              <div>
                <span className="text-lg font-extrabold text-[#F7F5EE] block">38</span>
                <span className="text-[10px] text-[#A0A8A3] uppercase">Classes</span>
              </div>
              <div>
                <span className="text-lg font-extrabold text-[#D6A434] block">224px</span>
                <span className="text-[10px] text-[#A0A8A3] uppercase">Resolution</span>
              </div>
              <div>
                <span className="text-lg font-extrabold text-[#2E8B67] block">&lt;200ms</span>
                <span className="text-[10px] text-[#A0A8A3] uppercase">Inference</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. TRUST & ARCHITECTURE STRIP */}
      <section className="bento-card p-6 bg-white">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div className="space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">EfficientNet-B0</span>
            <p className="text-xs text-[#6B756F]">Production Vision Backbone</p>
          </div>
          <div className="space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">99.43%</span>
            <p className="text-xs text-[#6B756F]">Test Macro Accuracy</p>
          </div>
          <div className="space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">Zero GenAI</span>
            <p className="text-xs text-[#6B756F]">No Hallucinated Advice</p>
          </div>
          <div className="space-y-1">
            <span className="text-2xl font-extrabold text-[#1F694B]">100% Verified</span>
            <p className="text-xs text-[#6B756F]">USDA / UC IPM / Cornell</p>
          </div>
        </div>
      </section>

      {/* 3. HOW AGROAI WORKS — 3-Step Horizontal Bento Sequence */}
      <section className="space-y-6">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
            Three Simple Steps
          </span>
          <h2 className="text-3xl font-bold text-[#1C231F] tracking-tight">
            How AgroAI Evaluates Your Crop
          </h2>
          <p className="text-sm text-[#6B756F]">
            Designed for farmers, researchers, and agronomists seeking fast, reproducible foliar disease screening.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Step 1 */}
          <div className="bento-card p-8 flex flex-col justify-between group hover:border-[#1F694B]">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] font-bold text-lg mb-6 group-hover:scale-105 transition-transform">
                01
              </div>
              <h3 className="font-bold text-xl text-[#1C231F] mb-2">Upload Clear Photo</h3>
              <p className="text-sm text-[#6B756F] leading-relaxed">
                Take a close-up photo of the affected plant leaf under natural daylight. Drag and drop or browse directly from your phone or computer.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-xs font-semibold text-[#1F694B]">
              JPG, PNG, WEBP supported
            </div>
          </div>

          {/* Step 2 */}
          <div className="bento-card p-8 flex flex-col justify-between group hover:border-[#1F694B]">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] font-bold text-lg mb-6 group-hover:scale-105 transition-transform">
                02
              </div>
              <h3 className="font-bold text-xl text-[#1C231F] mb-2">Model 1 Inference</h3>
              <p className="text-sm text-[#6B756F] leading-relaxed">
                EfficientNet-B0 applies exact ImageNet preprocessing and computes normalized softmax probabilities across all 38 PlantVillage crop conditions.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-xs font-semibold text-[#1F694B]">
              Top-3 Probabilities + Grad-CAM
            </div>
          </div>

          {/* Step 3 */}
          <div className="bento-card p-8 flex flex-col justify-between group hover:border-[#1F694B]">
            <div>
              <div className="w-12 h-12 rounded-2xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] font-bold text-lg mb-6 group-hover:scale-105 transition-transform">
                03
              </div>
              <h3 className="font-bold text-xl text-[#1C231F] mb-2">Verified Knowledge</h3>
              <p className="text-sm text-[#6B756F] leading-relaxed">
                Receive the prediction alongside verified symptoms, agronomic prevention measures, and university extension treatment options.
              </p>
            </div>
            <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-xs font-semibold text-[#1F694B]">
              Downloadable PDF Reports
            </div>
          </div>
        </div>
      </section>

      {/* 4. BENTO FEATURE GRID */}
      <section className="space-y-6">
        <div className="text-center max-w-xl mx-auto space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
            Core Architecture
          </span>
          <h2 className="text-3xl font-bold text-[#1C231F] tracking-tight">
            Built for Scientific Reliability
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
          {/* Bento Card 1: Confidence & Uncertainty (8 cols) */}
          <div className="md:col-span-8 bento-card p-8 bg-white flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-[#1F694B]">
                <Cpu className="w-5 h-5 text-[#D6A434]" />
                <span className="text-xs font-bold uppercase tracking-wider">Calibration & Safety</span>
              </div>
              <h3 className="text-2xl font-bold text-[#1C231F]">
                Calibrated Model Confidence with Uncertainty Alerts
              </h3>
              <p className="text-sm text-[#6B756F] leading-relaxed max-w-2xl">
                We never hide model uncertainty or present predictions as medical certitudes. When prediction confidence falls below 70%, the interface shifts into an advisory warning state, advising grower verification before chemical application.
              </p>
            </div>

            <div className="mt-8 pt-4 border-t border-[rgba(28,35,31,0.06)] flex items-center gap-6 text-xs text-[#6B756F]">
              <span>Explicit confidence thresholds</span>
              <span>•</span>
              <span>Top-3 class distribution</span>
            </div>
          </div>

          {/* Bento Card 2: Grad-CAM Explainability (4 cols) */}
          <div className="md:col-span-4 bento-card p-8 bg-[#1F694B] text-white flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-[#D6A434]">
                <Layers className="w-5 h-5" />
                <span className="text-xs font-bold uppercase tracking-wider">Explainability</span>
              </div>
              <h3 className="text-2xl font-bold text-white">
                Grad-CAM Visual Heatmaps
              </h3>
              <p className="text-xs text-white/80 leading-relaxed">
                See exactly which regions of the leaf blade influenced Model 1&apos;s classification decision via convolutional feature attribution.
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-white/10 text-xs text-[#E7F0EA]">
              Target Layer: conv_head
            </div>
          </div>

          {/* Bento Card 3: No-GenAI Knowledge Base (6 cols) */}
          <div className="md:col-span-6 bento-card p-8 bg-white flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-[#1F694B]">
                <BookOpen className="w-5 h-5 text-[#2E8B67]" />
                <span className="text-xs font-bold uppercase tracking-wider">Zero Generative AI</span>
              </div>
              <h3 className="text-xl font-bold text-[#1C231F]">
                Authoritative Agricultural Extension Facts
              </h3>
              <p className="text-sm text-[#6B756F] leading-relaxed">
                AgroAI deliberately omits conversational AI chatbots. All disease descriptions, symptoms, prevention checklists, and treatments are static, peer-reviewed facts from the USDA, UC IPM, Penn State, and Cornell University.
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-xs text-[#2E8B67] font-semibold">
              Zero hallucinated dosages or phantom pesticides
            </div>
          </div>

          {/* Bento Card 4: Formal PDF Reports (6 cols) */}
          <div className="md:col-span-6 bento-card p-8 bg-white flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-[#1F694B]">
                <FileText className="w-5 h-5 text-[#D6A434]" />
                <span className="text-xs font-bold uppercase tracking-wider">Documentation</span>
              </div>
              <h3 className="text-xl font-bold text-[#1C231F]">
                1-Click Exportable PDF Screening Reports
              </h3>
              <p className="text-sm text-[#6B756F] leading-relaxed">
                Generate clean, publication-ready diagnostic summary PDFs containing scan timestamps, confidence breakdowns, top-3 candidates, and agricultural management guidelines for field records.
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-xs text-[#1F694B] font-semibold">
              Built with ReportLab Python Engine
            </div>
          </div>
        </div>
      </section>

      {/* 5. SUPPORTED CROPS OVERVIEW */}
      <section className="bento-card p-8 sm:p-12 bg-white">
        <div className="max-w-3xl mb-8 space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
            Supported Scope
          </span>
          <h2 className="text-3xl font-bold text-[#1C231F] tracking-tight">
            38 Classes Across 14 Essential Crops
          </h2>
          <p className="text-sm text-[#6B756F]">
            Model 1 is specifically trained on 54,284 PlantVillage color images. We do not claim universal plant identification — we specialize in high-impact foliar screening.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3">
          {[
            { crop: 'Tomato', count: '10 conditions' },
            { crop: 'Apple', count: '4 conditions' },
            { crop: 'Corn (Maize)', count: '4 conditions' },
            { crop: 'Grape', count: '4 conditions' },
            { crop: 'Potato', count: '3 conditions' },
            { crop: 'Cherry', count: '2 conditions' },
            { crop: 'Bell Pepper', count: '2 conditions' },
            { crop: 'Peach', count: '2 conditions' },
            { crop: 'Strawberry', count: '2 conditions' },
            { crop: 'Orange', count: 'Citrus greening' },
            { crop: 'Squash', count: 'Powdery mildew' },
            { crop: 'Blueberry', count: 'Healthy check' },
            { crop: 'Raspberry', count: 'Healthy check' },
            { crop: 'Soybean', count: 'Healthy check' },
          ].map((item) => (
            <div
              key={item.crop}
              className="p-4 rounded-2xl bg-[#F7F5EE] border border-[rgba(28,35,31,0.06)] text-center space-y-1 hover:border-[#1F694B] transition-colors"
            >
              <p className="font-bold text-xs text-[#1C231F] truncate">{item.crop}</p>
              <span className="text-[10px] text-[#6B756F] block">{item.count}</span>
            </div>
          ))}
        </div>

        <div className="mt-8 pt-6 border-t border-[rgba(28,35,31,0.06)] text-center">
          <Link
            href="/diseases"
            className="inline-flex items-center gap-1.5 text-xs font-bold text-[#1F694B] hover:underline"
          >
            <span>Browse Complete 38-Class Reference Library</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </section>

      {/* 6. FAQ SECTION */}
      <section className="space-y-6 max-w-4xl mx-auto">
        <div className="text-center space-y-2">
          <span className="text-xs font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-3 py-1 rounded-full">
            Frequently Asked Questions
          </span>
          <h2 className="text-3xl font-bold text-[#1C231F] tracking-tight">
            Understanding AgroAI
          </h2>
        </div>

        <div className="space-y-4">
          {[
            {
              q: 'Why does AgroAI not use a Generative AI chatbot?',
              a: 'Generative AI language models are prone to hallucinating non-existent chemical treatments, incorrect pesticide dosages, and false diagnoses that could severely damage crops or violate environmental laws. AgroAI uses a dedicated computer vision model (EfficientNet-B0) paired with verified, peer-reviewed extension facts.',
            },
            {
              q: 'What is the benchmark accuracy of Model 1?',
              a: 'Model 1 achieved 99.43% test accuracy and 99.14% macro F1 on the clean PlantVillage dataset (54,284 images). Note that real-world field conditions with variable shadows and dirt may exhibit lower confidence, which is why we display calibrated confidence ratings and uncertainty warnings.',
            },
            {
              q: 'Can AgroAI identify any houseplant or weed?',
              a: 'No. AgroAI Model 1 is specialized on 38 specific agricultural crop classes (Tomatoes, Apples, Corn, Potatoes, Grapes, Citrus, etc.). We intentionally reject claiming universal plant recognition to maintain scientific integrity.',
            },
            {
              q: 'How should I take a leaf photo for best results?',
              a: 'Place a single affected leaf against a neutral background (or isolate it gently in the field) under good, even lighting. Ensure the focal point is crisp and shows characteristic lesions or spots.',
            },
          ].map((faq, i) => (
            <div key={i} className="bento-card p-6 bg-white space-y-2">
              <h4 className="font-bold text-sm text-[#1C231F] flex items-center justify-between">
                <span>{faq.q}</span>
              </h4>
              <p className="text-xs sm:text-sm text-[#6B756F] leading-relaxed">
                {faq.a}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 7. FINAL CALL TO ACTION BANNER */}
      <section className="bento-card p-10 sm:p-14 bg-gradient-to-r from-[#1F694B] to-[#2E8B67] text-white text-center relative overflow-hidden">
        <div className="max-w-2xl mx-auto space-y-6 relative z-10">
          <h2 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            Ready to Screen Your Crop?
          </h2>
          <p className="text-sm sm:text-base text-[#F7F5EE]/90 leading-relaxed">
            Upload your leaf photo now and receive instant Model 1 classification, confidence scoring, and verified agricultural guidance.
          </p>
          <div className="pt-2">
            <Link
              href="/scan"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-full bg-white text-[#1F694B] text-base font-bold shadow-lg hover:bg-[#F7F5EE] transition-all active:scale-[0.98]"
            >
              <Scan className="w-5 h-5 text-[#D6A434]" />
              <span>Launch AI Leaf Scan</span>
            </Link>
          </div>
        </div>

        {/* Ambient background rings */}
        <div className="absolute top-0 right-0 w-80 h-80 rounded-full border border-white/10 -mr-20 -mt-20 pointer-events-none" />
        <div className="absolute bottom-0 left-0 w-80 h-80 rounded-full border border-white/10 -ml-20 -mb-20 pointer-events-none" />
      </section>
    </div>
  );
}
