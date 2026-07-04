---
title: BhashaBridge Backend
emoji: 🌉
colorFrom: indigo
colorTo: green
sdk: docker
app_port: 8000
pinned: false
license: mit
---

# BhashaBridge Backend

Multilingual translation API for Indian languages and low-resource dialects.

- **Stack**: FastAPI + NLLB-200 (any-to-any) + IndicTrans2 (Indic→English) + flan-t5 refinement + FAISS RAG.
- **Auth**: send header `X-API-Key: <API_KEY>` (set as a Space secret).
- **Endpoint**: `POST /api/v1/translate` with `{"text": "...", "source_language": "auto", "target_language": "hindi"}`.
- **Health**: `GET /api/v1/health`.

This Space is built from the [BhashaBridge repo](https://github.com/vivekkashyap17/BhashaBridge) `backend/` directory. It runs on the free CPU tier; the first request after an idle period is slow while the ~5 GB of models load.
