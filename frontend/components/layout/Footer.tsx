import React from 'react';
import Link from 'next/link';
import { Leaf, ShieldCheck, Cpu, Database, ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="w-full bg-[#1C231F] text-[#F7F5EE] mt-24 border-t border-[#1C231F]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-10">
          {/* Brand Col */}
          <div className="space-y-4 md:col-span-1">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-[#1F694B] flex items-center justify-center text-white">
                <Leaf className="w-5 h-5 text-[#F7F5EE]" />
              </div>
              <span className="font-bold text-2xl tracking-tight text-white">AgroAI</span>
            </div>
            <p className="text-sm text-[#A0A8A3] leading-relaxed">
              Scan. Understand. Protect. Production-grade plant disease detection powered by Model 1 EfficientNet-B0 and verified agricultural facts.
            </p>
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/5 border border-white/10 text-xs text-[#2E8B67]">
              <ShieldCheck className="w-3.5 h-3.5 text-[#D6A434]" />
              <span>Strictly No Generative AI in V1</span>
            </div>
          </div>

          {/* Navigation */}
          <div>
            <h4 className="font-semibold text-white text-sm uppercase tracking-wider mb-4">Platform</h4>
            <ul className="space-y-2.5 text-sm text-[#A0A8A3]">
              <li><Link href="/scan" className="hover:text-white transition-colors">AI Leaf Scan</Link></li>
              <li><Link href="/diseases" className="hover:text-white transition-colors">38 Supported Diseases</Link></li>
              <li><Link href="/history" className="hover:text-white transition-colors">Scan History</Link></li>
              <li><Link href="/about" className="hover:text-white transition-colors">Model Transparency</Link></li>
            </ul>
          </div>

          {/* Model Transparency */}
          <div>
            <h4 className="font-semibold text-white text-sm uppercase tracking-wider mb-4">Production Model</h4>
            <ul className="space-y-2.5 text-xs text-[#A0A8A3]">
              <li className="flex items-center gap-2">
                <Cpu className="w-3.5 h-3.5 text-[#D6A434]" />
                <span>Model: EfficientNetV2-S</span>
              </li>
              <li className="flex items-center gap-2">
                <Database className="w-3.5 h-3.5 text-[#2E8B67]" />
                <span>Test Accuracy: 99.58%</span>
              </li>
              <li>Grad-CAM Layer: features.7</li>
              <li>Resolution: 384×384 RGB</li>
              <li>Classes: 38 PlantVillage Conditions</li>
              <li>Rollback Safety: Archived B0 Retained</li>
            </ul>
          </div>

          {/* Verified Sources */}
          <div>
            <h4 className="font-semibold text-white text-sm uppercase tracking-wider mb-4">Knowledge Sources</h4>
            <p className="text-xs text-[#A0A8A3] leading-relaxed mb-3">
              Disease symptoms, prevention methods, and treatment options are curated exclusively from peer-reviewed agricultural extension guides:
            </p>
            <ul className="space-y-1.5 text-xs text-[#E7F0EA]/80">
              <li>• USDA Agricultural Research Service</li>
              <li>• University of California IPM</li>
              <li>• Cornell University Cooperative Extension</li>
              <li>• Penn State College of Agricultural Sciences</li>
            </ul>
          </div>
        </div>

        {/* Disclaimer Strip */}
        <div className="mt-14 pt-8 border-t border-white/10 text-center md:flex md:justify-between md:items-center text-xs text-[#A0A8A3]">
          <p>© {new Date().getFullYear()} AgroAI Platform. Built with Bento Grid Design System.</p>
          <p className="mt-2 md:mt-0 text-[11px] max-w-xl text-[#8E9792]">
            Diagnostic Disclaimer: AgroAI provides screening predictions based on model probabilities. This tool does not substitute for certified lab assays. Always follow local agricultural chemical safety guidelines.
          </p>
        </div>
      </div>
    </footer>
  );
}

