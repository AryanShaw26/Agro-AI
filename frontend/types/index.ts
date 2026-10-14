export interface TopPrediction {
  crop: string;
  disease: string;
  confidence: number;
  is_healthy: boolean;
  slug: string;
  raw_class?: string;
}

export interface TreatmentItem {
  treatment_type: string;
  description: string;
  safety_note?: string | null;
}

export interface ReferenceItem {
  title: string;
  publisher: string;
  url?: string | null;
}

export interface KnowledgeData {
  available: boolean;
  overview?: string | null;
  causal_agent?: string | null;
  severity?: string | null;
  safety_notes?: string | null;
  verified_source?: string | null;
  symptoms: string[];
  preventions: string[];
  treatments: TreatmentItem[];
  references: ReferenceItem[];
}

export interface PredictionResult {
  prediction_id: string;
  crop: string;
  disease: string;
  confidence: number;
  confidence_state: 'confident' | 'uncertain';
  is_healthy: boolean;
  raw_class: string;
  slug: string;
  model_version: string;
  processing_time_ms: number;
  top_predictions: TopPrediction[];
  knowledge: KnowledgeData;
  gradcam_image?: string | null;
  image_preview_url?: string | null;
}

export interface DiseaseListItem {
  id: string;
  raw_class: string;
  crop: string;
  disease_name: string;
  slug: string;
  is_healthy: boolean;
  severity?: string | null;
  overview: string;
  verified_source: string;
}

export interface DiseaseDetail extends DiseaseListItem {
  causal_agent?: string | null;
  safety_notes?: string | null;
  symptoms: string[];
  preventions: string[];
  treatments: TreatmentItem[];
  references: ReferenceItem[];
}

export interface ScanHistoryRecord {
  id: string;
  created_at: string;
  crop: string;
  disease: string;
  raw_class: string;
  confidence: number;
  confidence_state: string;
  model_version: string;
  processing_time_ms: number;
  image_data_uri?: string | null;
  top_predictions: TopPrediction[];
}

