# AgroAI — Plant Disease Detection Platform
**Model 1: EfficientNet-B0 • Bento Grid Design System • No Generative AI**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-1F694B?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-2E8B67?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.2%2B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)

---

## 🌿 Product Vision & Architecture

AgroAI is a production-grade, accessible agricultural screening platform built around **Model 1 (EfficientNet-B0)**. When a user uploads a plant leaf photo, the system evaluates the image across **38 PlantVillage crop conditions** and pairs the model's confidence distribution with authoritative, peer-reviewed extension facts from a verified relational database.

### Strict No-GenAI Guarantee
AgroAI V1 **strictly excludes Generative AI chatbots and LLM-written prescriptions**. Agricultural guidance (disease overview, symptoms, cultural prevention, and chemical management) is deterministic and verified against university extension manuals (USDA-ARS, UC IPM, Penn State Extension, Cornell AgriTech).

```
[ User Browser / Next.js ]
         │
         ▼  (Multipart Image POST)
[ Stable REST API: POST /api/v1/predict ]
         │
         ▼
[ Inference Layer & Model Registry ]
         │
         ├──► [ Model 1: EfficientNet-B0 (38 Classes) ] ──► Probabilities (Top-1 + Top-3)
         │                                                    │
         ├──► [ Grad-CAM Module (conv_head) ] ──────────────► Activation Heatmap
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
- **Micro-Interactions**: Subtle 2–4px card lift, smooth scanning line overlay during inference, and tabbed Grad-CAM inspection.

---

## 🧪 Model 1 Specifications

| Metric / Parameter | Value |
|---|---|
| **Architecture** | EfficientNet-B0 (Pretrained on ImageNet, Fine-tuned for PlantVillage) |
| **Classifier** | `Linear(in_features=1280, out_features=38)` |
| **Total Parameters** | 4,056,226 |
| **Best Checkpoint** | `Models/efficientnet_b0_best.pth` |
| **Best Epoch** | Epoch 8 |
| **Validation Macro F1** | **99.42%** |
| **Test Accuracy** | **99.43%** |
| **Macro Precision** | **98.95%** |
| **Macro Recall** | **99.40%** |
| **Macro F1** | **99.14%** |
| **Input Shape** | `[1, 3, 224, 224]` RGB |
| **Normalization** | ImageNet Mean `[0.485, 0.456, 0.406]`, Std `[0.229, 0.224, 0.225]` |

### Supported Crops (38 Classes)
- **Apple**: Apple Scab, Black Rot, Cedar Apple Rust, Healthy
- **Blueberry**: Healthy
- **Cherry**: Powdery Mildew, Healthy
- **Corn (Maize)**: Cercospora Leaf Spot / Gray Leaf Spot, Common Rust, Northern Leaf Blight, Healthy
- **Grape**: Black Rot, Esca (Black Measles), Leaf Blight (Isariopsis Leaf Spot), Healthy
- **Orange**: Huanglongbing (Citrus Greening)
- **Peach**: Bacterial Spot, Healthy
- **Bell Pepper**: Bacterial Spot, Healthy
- **Potato**: Early Blight, Late Blight, Healthy
- **Raspberry**: Healthy
- **Soybean**: Healthy
- **Squash**: Powdery Mildew
- **Strawberry**: Leaf Scorch, Healthy
- **Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Two-spotted Spider Mites, Target Spot, Tomato Yellow Leaf Curl Virus, Tomato Mosaic Virus, Healthy

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 2. Backend Setup
```bash
# From workspace root
# Install backend dependencies
python -m uv pip install -r backend/requirements.txt

# Run backend API server (runs on http://127.0.0.1:8000)
$env:PYTHONPATH='backend'; .venv\Scripts\python.exe backend/run.py
```
*The knowledge base automatically seeds all 38 classes upon initial startup.*
Interactive Swagger docs are available at **`http://127.0.0.1:8000/docs`**.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open **`http://localhost:3000`** in your browser to experience AgroAI.

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
  "model_version": "efficientnet-b0-v1",
  "processing_time_ms": 142.3,
  "top_predictions": [
    { "crop": "Tomato", "disease": "Early Blight", "confidence": 0.9943, "is_healthy": false, "slug": "tomato-early-blight" },
    { "crop": "Tomato", "disease": "Late Blight", "confidence": 0.0032, "is_healthy": false, "slug": "tomato-late-blight" },
    { "crop": "Tomato", "disease": "Leaf Mold", "confidence": 0.0011, "is_healthy": false, "slug": "tomato-leaf-mold" }
  ],
  "knowledge": {
    "available": true,
    "overview": "Early blight is one of the most common fungal diseases affecting tomatoes...",
    "causal_agent": "Alternaria linariae",
    "severity": "Moderate to High",
    "safety_notes": "Stem cankers on seedlings can girdle and kill young transplants.",
    "verified_source": "Cornell University Cooperative Extension",
    "symptoms": ["..."],
    "preventions": ["..."],
    "treatments": [
      {
        "treatment_type": "Fungicide Spray",
        "description": "Apply protectant fungicides (chlorothalonil, copper) on 7-14 day intervals.",
        "safety_note": "Follow pre-harvest intervals on label."
      }
    ],
    "references": [{"title": "Tomato Early Blight Factsheet", "publisher": "Cornell Extension"}]
  },
  "gradcam_image": "data:image/jpeg;base64,...",
  "image_preview_url": "data:image/jpeg;base64,..."
}
```

### Additional Endpoints
- `GET /api/v1/diseases`: Filter and search all 38 supported classes.
- `GET /api/v1/diseases/{slug}`: Full verified agricultural guide for any condition.
- `GET /api/v1/history`: Local scan history records with pagination.
- `GET /api/v1/reports/{prediction_id}/pdf`: Dynamically generated PDF screening report.
- `GET /health`: Platform health, active model version, and verified class count.

---

## 📄 License & Agronomic Disclaimer
AgroAI is designed as an informational screening tool. Predictions do not replace certified agricultural laboratory diagnostics. Always follow chemical safety labels and consult regional agricultural extension agents.

