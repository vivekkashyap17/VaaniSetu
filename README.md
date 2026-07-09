# VaaniSetu

Multilingual translation service for Indian languages — including low-resource
regional dialects — powered by NLLB-200 and IndicTrans2.

## Overview

VaaniSetu translates text between global languages, 19 major Indian languages,
and 5 low-resource regional dialects. It auto-detects the source language,
transliterates roman-Hindi input to Devanagari, retrieves semantic context with
a FAISS vector store, translates with the best engine for the language pair, and
refines the English output with an LLM.

## Features

- **Any-to-any translation** — NLLB-200 for general pairs, IndicTrans2 for Indic→English
- **Automatic language detection** with an explicit source-language override
- **Roman-Hindi → Devanagari** transliteration
- **Low-resource dialects** — Bhojpuri, Awadhi, Maithili, Magahi, Chhattisgarhi
- **RAG context** via FAISS + sentence embeddings
- **LLM refinement** of translated output
- **API-key auth** and per-route rate limiting

## Supported Languages

- **Global (7):** English, French, Spanish, German, Arabic, Chinese, Russian
- **Indian (19):** Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Punjabi,
  Kannada, Malayalam, Urdu, Odia, Assamese, Nepali, Sanskrit, Konkani, Sindhi,
  Kashmiri, Manipuri, Santali
- **Regional dialects (5):** Bhojpuri, Awadhi, Maithili, Magahi, Chhattisgarhi

## Tech Stack

- **Backend:** FastAPI, PyTorch (CPU), NLLB-200, IndicTrans2, flan-t5, FAISS, SQLite
- **Frontend:** React + Vite
- **Deployment:** Hugging Face Spaces (backend) · Vercel (frontend) · Docker Compose (local)

## How It Works

1. Detect the source language (or use the explicit override)
2. Transliterate roman-Hindi input to Devanagari
3. Retrieve semantic context from the FAISS index
4. Translate with the engine best suited to the language pair
5. Refine the English output with an LLM
6. Return the translation with metadata (confidence, timing, context)

## Getting Started (local)

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then edit values (set your API_KEY)
uvicorn app.main:app --reload
```
The API runs at `http://localhost:8000` (docs at `/docs`). The first request
loads ~5 GB of models, so it is slow on cold start.

### Frontend
```bash
cd frontend
npm install
cp .env.example .env          # set VITE_API_BASE_URL and VITE_API_KEY (must match backend API_KEY)
npm run dev
```

### Docker (both services)
```bash
cd backend
cp .env.example .env          # set API_KEY
export HF_TOKEN=<your-hf-token>   # for the gated IndicTrans2 model
docker compose up --build     # backend on :8000, frontend on :5173
```

## API Usage

```bash
curl -X POST http://localhost:8000/api/v1/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: <your-api-key>" \
  -d '{"text": "Hello, how are you?", "source_language": "auto", "target_language": "hindi"}'
```

`source_language` accepts `"auto"` or any supported language name;
`target_language` accepts any supported language name.

## Project Structure

```
VaaniSetu/
├── backend/               # FastAPI translation API
│   ├── app/               # routes, pipeline, services, models, config
│   ├── tests/             # pytest suite
│   ├── deploy/            # Hugging Face Space deploy script
│   ├── docker-compose.yml # runs backend + frontend locally
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/              # React + Vite SPA
│   ├── src/
│   ├── Dockerfile
│   └── nginx.conf
├── DEPLOY.md              # step-by-step deployment guide
└── LICENSE
```

## Testing

```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

## Deployment

See **[DEPLOY.md](DEPLOY.md)** for deploying the backend to Hugging Face Spaces
and the frontend to Vercel.

> **Note on the API key:** the frontend's `VITE_API_KEY` is baked into the
> browser bundle, so it is inherently public. It is a lightweight gate and
> rate-limit key, not a true secret — do not reuse it for anything sensitive.

## License

Released under the [MIT License](LICENSE).

## Acknowledgements

- [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M) — Meta AI
- [IndicTrans2](https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M) — AI4Bharat
- [flan-t5](https://huggingface.co/google/flan-t5-base) — Google
