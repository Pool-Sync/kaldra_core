# KALDRA — Production Architecture Overview

## High-Level Flow

User → Vercel Frontend → Render API Gateway → Master Engine V2 → Response

## Components

### Frontend (Next.js / Vercel)
- UI
- API client
- Visual Engine (futuro)

### Backend (FastAPI / Render)
- Endpoints
- Painlevé + TW
- Delta144
- Kindra
- Bias engine

### Data Lab Workers (Render Jobs)
- News ingestion
- Earnings (futuro)
- Geopolitics ingestion

### External APIs
- MediaStack
- GNews

## Observability
- Logging estruturado no backend
- Logs do Render
- Logs do Vercel (frontend)
