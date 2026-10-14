'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { History, Trash2, Download, ArrowRight, RefreshCw, Calendar, Sparkles, AlertCircle } from 'lucide-react';
import { ScanHistoryRecord } from '@/types';
import { getScanHistory, deleteScanRecord, getReportPdfUrl } from '@/lib/api';

export default function ScanHistoryList() {
  const [history, setHistory] = useState<ScanHistoryRecord[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const data = await getScanHistory({ limit: 50 });
      setHistory(data.scans);
      setTotal(data.total);
    } catch (err) {
      console.error('Failed to load scan history:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to remove this scan from your history?')) return;
    try {
      setDeletingId(id);
      await deleteScanRecord(id);
      setHistory((prev) => prev.filter((item) => item.id !== id));
      setTotal((prev) => Math.max(0, prev - 1));
    } catch (err) {
      alert('Failed to delete scan record.');
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="w-full space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-[#1C231F] tracking-tight">Your Recent Scans</h2>
          <p className="text-xs text-[#6B756F]">
            {total} total plant screening records preserved locally
          </p>
        </div>

        <Link
          href="/scan"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#1F694B] text-white text-xs font-semibold hover:bg-[#18533b] transition-all self-start sm:self-auto"
        >
          <Sparkles className="w-3.5 h-3.5 text-[#D6A434]" />
          <span>New Leaf Scan</span>
        </Link>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <RefreshCw className="w-8 h-8 text-[#1F694B] animate-spin mb-3" />
          <p className="text-sm font-medium text-[#6B756F]">Loading saved scans...</p>
        </div>
      ) : history.length === 0 ? (
        <div className="bento-card p-12 text-center bg-white">
          <div className="w-16 h-16 rounded-3xl bg-[#E7F0EA] flex items-center justify-center text-[#1F694B] mx-auto mb-4">
            <History className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-[#1C231F] mb-1">Your scans will appear here</h3>
          <p className="text-xs text-[#6B756F] max-w-sm mx-auto mb-6">
            Whenever you screen a plant leaf with Model 1, the prediction, confidence, and verified advice are saved to your local history.
          </p>
          <Link
            href="/scan"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-[#1F694B] text-white text-xs font-semibold hover:bg-[#18533b] transition-all"
          >
            <span>Start First Scan</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {history.map((scan) => {
            const dateStr = new Date(scan.created_at).toLocaleDateString(undefined, {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            });
            const isUncertain = scan.confidence_state === 'uncertain';
            const isHealthy = scan.disease.toLowerCase().includes('healthy');

            return (
              <div
                key={scan.id}
                className="bento-card p-5 flex flex-col justify-between space-y-4 hover:border-[#1F694B]/40 transition-all"
              >
                <div className="flex items-start gap-4">
                  {/* Thumbnail */}
                  <div className="w-20 h-20 rounded-2xl overflow-hidden bg-[#1C231F]/5 border border-[rgba(28,35,31,0.08)] shrink-0">
                    <img
                      src={scan.image_data_uri || '/placeholder-leaf.jpg'}
                      alt={scan.disease}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Details */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-[#1F694B] bg-[#E7F0EA] px-2 py-0.5 rounded-full">
                        {scan.crop}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isHealthy
                          ? 'bg-[#1F694B]/10 text-[#1F694B]'
                          : isUncertain
                          ? 'bg-[#B7791F]/10 text-[#B7791F]'
                          : 'bg-[#1C231F]/10 text-[#1C231F]'
                      }`}>
                        {(scan.confidence * 100).toFixed(1)}% ({scan.confidence_state})
                      </span>
                    </div>

                    <h4 className="font-bold text-sm text-[#1C231F] truncate">
                      {scan.disease}
                    </h4>

                    <div className="flex items-center gap-2 text-[11px] text-[#6B756F] mt-1">
                      <Calendar className="w-3 h-3" />
                      <span>{dateStr}</span>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="pt-3 border-t border-[rgba(28,35,31,0.06)] flex items-center justify-between">
                  <a
                    href={getReportPdfUrl(scan.id)}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F694B] hover:underline"
                  >
                    <Download className="w-3.5 h-3.5 text-[#D6A434]" />
                    <span>Download PDF</span>
                  </a>

                  <button
                    type="button"
                    onClick={() => handleDelete(scan.id)}
                    disabled={deletingId === scan.id}
                    className="p-1.5 rounded-lg text-[#6B756F] hover:text-[#B84A4A] hover:bg-red-50 transition-colors"
                    title="Delete record"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

