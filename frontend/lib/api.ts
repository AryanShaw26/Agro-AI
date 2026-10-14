import { PredictionResult, DiseaseListItem, DiseaseDetail, ScanHistoryRecord } from '@/types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';

export async function predictLeafImage(file: File, includeGradcam = true): Promise<PredictionResult> {
  const formData = new FormData();
  formData.append('image', file);
  formData.append('include_gradcam', includeGradcam ? 'true' : 'false');

  const res = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    let errorMsg = `Server error (${res.status})`;
    try {
      const errData = await res.json();
      if (errData.detail) errorMsg = errData.detail;
    } catch {
      // ignore
    }
    throw new Error(errorMsg);
  }

  return res.json();
}

export async function getPredictionById(id: string): Promise<PredictionResult> {
  const res = await fetch(`${API_BASE}/predictions/${id}`);
  if (!res.ok) {
    throw new Error(`Failed to load prediction ${id}`);
  }
  return res.json();
}

export async function getDiseases(params?: {
  crop?: string;
  search?: string;
  healthy_only?: boolean;
}): Promise<DiseaseListItem[]> {
  const searchParams = new URLSearchParams();
  if (params?.crop) searchParams.append('crop', params.crop);
  if (params?.search) searchParams.append('search', params.search);
  if (params?.healthy_only !== undefined) searchParams.append('healthy_only', String(params.healthy_only));

  const qs = searchParams.toString();
  const url = `${API_BASE}/diseases${qs ? `?${qs}` : ''}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error('Failed to load supported diseases');
  }
  return res.json();
}

export async function getDiseaseBySlug(slug: string): Promise<DiseaseDetail> {
  const res = await fetch(`${API_BASE}/diseases/${slug}`);
  if (!res.ok) {
    throw new Error(`Failed to load disease details for ${slug}`);
  }
  return res.json();
}

export async function getScanHistory(params?: {
  crop?: string;
  limit?: number;
  offset?: number;
}): Promise<{ total: number; scans: ScanHistoryRecord[] }> {
  const searchParams = new URLSearchParams();
  if (params?.crop) searchParams.append('crop', params.crop);
  if (params?.limit) searchParams.append('limit', String(params.limit));
  if (params?.offset) searchParams.append('offset', String(params.offset));

  const qs = searchParams.toString();
  const url = `${API_BASE}/history${qs ? `?${qs}` : ''}`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error('Failed to load scan history');
  }
  return res.json();
}

export async function deleteScanRecord(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/history/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) {
    throw new Error('Failed to delete scan record');
  }
}

export function getReportPdfUrl(predictionId: string): string {
  return `${API_BASE}/reports/${predictionId}/pdf`;
}
