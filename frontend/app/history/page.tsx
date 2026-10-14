'use client';

import React from 'react';
import ScanHistoryList from '@/components/history/ScanHistoryList';

export default function HistoryPage() {
  return (
    <div className="w-full max-w-5xl mx-auto py-6 sm:py-10 space-y-6">
      <ScanHistoryList />
    </div>
  );
}

