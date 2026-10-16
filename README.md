# AgroAI — Plant Disease Detection Platform
**Model: EfficientNetV2-S + Integrated Grad-CAM • Bento Grid Design System • No Generative AI**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-1F694B?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-2E8B67?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

---

## 🌿 Product Vision & Architecture

AgroAI is a production-grade, accessible agricultural screening platform powered by **EfficientNetV2-S with Integrated Grad-CAM**. When a user uploads a plant leaf photo, the system evaluates the image across **38 PlantVillage crop conditions** and pairs the model's confidence distribution with authoritative, peer-reviewed extension facts from a verified relational database.

### Strict No-GenAI Guarantee
AgroAI **strictly excludes Generative AI chatbots and LLM-written prescriptions**. Agricultural guidance (disease overview, symptoms, cultural prevention, and chemical management) is deterministic and verified against university extension manuals (USDA-ARS, UC IPM, Penn State Extension, Cornell AgriTech).

```
[ User Browser / Next.js ]
         │
         ▼  (Multipart Image POST)
[ Stable REST API: POST /api/v1/predict ]
         │
         ▼
[ Inference Layer & Model Registry ]
         │
         ├──► [ metadata.json ] ──► Dynamically configures size, mean, std & Grad-CAM layer
         │                                                    │
         ├──► [ EfficientNetV2-S (38 Classes) ] ────────────► Probabilities (Top-1 + Top-3)
         │                                                    │
         ├──► [ Integrated Grad-CAM (features.7) ] ─────────► Attention Overlay + Heatmap
         │
         ▼
[ PostgreSQL / SQLite Knowledge Base ] ─────────────────────► Verified Facts Only
         │
         ▼
[ Bento Result Dashboard & PDF Report Generator ]
```

---

## 🎨 Bento Grid Design System

- **Primary Colors**:
  - Forest Green: `#1F694B` (Primary brand, CTA buttons)
  - Emerald: `#2E8B67` (Accents, positive status)
  - Deep Charcoal: `#1C231F` (Headings, primary text)
  - Off-White: `#F7F5EE` (Canvas background)
  - Golden Yellow: `#D6A434` (Highlights, telemetry badge)
  - Soft Sage: `#E7F0EA` (Subtle bento surfaces)
  - Warning Amber: `#B7791F` (Low-confidence advisory state)
- **Grid Layout**: 12-column responsive Bento grid collapsing to a priority single column on mobile.
- **Explainability**: Integrated Grad-CAM with 4 interactive view modes (Side-by-Side, Overlay, Raw Heatmap, Original Leaf).

---

## 🧪 Model Specifications

| Metric / Parameter | EfficientNetV2-S (Active) | EfficientNet-B0 (Archived Rollback) |
|---|---|---|
| **Architecture** | EfficientNetV2-S | EfficientNet-B0 |
| **Status** | Active Production Model | Retained for Rollback |
| **Deployment Contract** | `Models/efficientnetv2_s_metadata.json` | Configurable |
| **Weights Checkpoint** | `Models/efficientnetv2_s_38class_gradcam_best.pth` | `Models/efficientnet_b0_best.pth` |
| **Grad-CAM Target Layer** | `features.7` (Integrated First-Class) | `conv_head` |
| **Benchmark Accuracy** | **99.58%** | 99.43% |
| **Macro F1 Score** | **99.36%** | 99.14% |
| **Input Shape** | `[1, 3, 384, 384]` RGB | `[1, 3, 224, 224]` RGB |
| **Classes Supported** | 38 PlantVillage Classes | 38 PlantVillage Classes |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# From workspace root
$env:PYTHONPATH='backend'; .venv\Scripts\python.exe backend/run.py
```
*API running on `http://127.0.0.1:8000` (Swagger docs: `http://127.0.0.1:8000/docs`).*

### 3. Frontend Setup
```bash
cd frontend
npm run dev
```
Open **`http://localhost:3000`** in your browser.

---

## 📡 API Contract Specification

### `POST /api/v1/predict`
Accepts `multipart/form-data` with an image file:
```json
{
  "prediction_id": "97e6821d-...",
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 0.9943,
  "confidence_state": "confident",
  "is_healthy": false,
  "raw_class": "Tomato___Early_blight",
  "slug": "tomato-early-blight",
  "model_version": "efficientnetv2-s-gradcam-v1",
  "processing_time_ms": 142.3,
  "top_predictions": [
    { "crop": "Tomato", "disease": "Early Blight", "confidence": 0.9943, "is_healthy": false, "slug": "tomato-early-blight" },
    { "crop": "Tomato", "disease": "Late Blight", "confidence": 0.0032, "is_healthy": false, "slug": "tomato-late-blight" },
    { "crop": "Tomato", "disease": "Leaf Mold", "confidence": 0.0011, "is_healthy": false, "slug": "tomato-leaf-mold" }
  ],
  "gradcam": {
    "available": true,
    "target_class": "Tomato___Early_blight",
    "overlay_url": "/api/v1/predictions/97e6821d-.../gradcam",
    "heatmap_url": "/api/v1/predictions/97e6821d-.../gradcam/heatmap",
    "overlay_base64": "data:image/jpeg;base64,..."
  },
  "knowledge": {
    "available": true,
    "overview": "Early blight is one of the most common fungal diseases affecting tomatoes...",
    "causal_agent": "Alternaria linariae",
    "severity": "Moderate to High",
    "verified_source": "Cornell University Cooperative Extension"
  }
}
```

### Additional Endpoints
- `GET /api/v1/model`: Returns deployment metadata contract and active architecture details.
- `GET /api/v1/predictions/{id}/gradcam`: Streams Grad-CAM blended overlay JPEG.
- `GET /api/v1/predictions/{id}/gradcam/heatmap`: Streams raw Grad-CAM Jet heatmap JPEG.
- `GET /api/v1/diseases`: Filter and search all 38 supported classes.
- `GET /api/v1/diseases/{slug}`: Full verified agricultural guide for any condition.
- `GET /api/v1/history`: Local scan history records with pagination.
- `GET /api/v1/reports/{prediction_id}/pdf`: Dynamically generated PDF screening report.
- `GET /health`: Platform health, active model version, and Grad-CAM integration status.

---

## 📄 License & Agronomic Disclaimer
AgroAI is designed as an informational screening tool. Predictions do not replace certified agricultural laboratory diagnostics. Always follow chemical safety labels and consult regional agricultural extension agents.
