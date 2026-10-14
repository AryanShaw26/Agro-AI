'use client';

import React from 'react';
import { BarChart3, HelpCircle } from 'lucide-react';
import { TopPrediction } from '@/types';

interface TopPredictionsProps {
  topPredictions: TopPrediction[];
}

export default function TopPredictions({ topPredictions }: TopPredictionsProps) {
  return (
    <div className="bento-card p-6 h-full flex flex-col justify-between">
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B]">
              <BarChart3 className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-base text-[#1C231F]">Top Candidate Predictions</h3>
          </div>
          <div className="group relative">
            <HelpCircle className="w-4 h-4 text-[#6B756F] cursor-pointer" />
            <div className="absolute right-0 top-6 w-64 p-3 bg-[#1C231F] text-white text-xs rounded-xl shadow-xl opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-30 leading-normal">
              These percentages represent Model 1's softmax probability distribution over the 38 supported classes, not an absolute diagnosis.
            </div>
          </div>
        </div>

        <p className="text-xs text-[#6B756F] mb-5">
          Model 1 evaluation ranked by classification probability:
        </p>

        {/* Prediction Bars */}
        <div className="space-y-4">
          {topPredictions.map((pred, index) => {
            const pct = (pred.confidence * 100).toFixed(1);
            const isRank1 = index === 0;

            return (
              <div key={index} className="space-y-1.5">
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2 min-w-0">
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center font-bold text-[10px] ${
                      isRank1 ? 'bg-[#1F694B] text-white' : 'bg-[#E7F0EA] text-[#6B756F]'
                    }`}>
                      {index + 1}
                    </span>
                    <span className={`font-semibold truncate ${isRank1 ? 'text-[#1C231F]' : 'text-[#6B756F]'}`}>
                      {pred.crop} — {pred.disease}
                    </span>
                  </div>
                  <span className="font-mono font-bold text-[#1C231F] ml-2 shrink-0">
                    {pct}%
                  </span>
                </div>

                {/* Progress Meter Bar */}
                <div className="w-full h-2.5 rounded-full bg-[#E7F0EA] overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      isRank1 ? 'bg-[#1F694B]' : 'bg-[#2E8B67]/40'
                    }`}
                    style={{ width: `${Math.max(Number(pct), 2)}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="mt-6 pt-4 border-t border-[rgba(28,35,31,0.06)] text-[11px] text-[#6B756F] flex items-center justify-between">
        <span>Softmax Normalized</span>
        <span>Top 3 of 38 Classes</span>
      </div>
    </div>
  );
}
