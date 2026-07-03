# CLAUDE.md - BhashaBridge

System architecture blueprint and token-saving caching guardrails for Claude Code.

## 🛠 Development Workflow Commands
- **Install Deps**: `pip install -r requirements.txt` (Run from `backend/` inside active `.venv`)
- **Run API**: `uvicorn app.main:app --reload`
- **Run via Docker**: `export HF_TOKEN=<token>` then `docker compose up --build` (from `backend/`). The image is CPU-only; `docker-compose.yml` mounts the host HF cache (`~/.cache/huggingface`) so models aren't re-downloaded, reads config from `.env`, and serves on `:8000`. `.env` is never baked into the image (see `.dockerignore`); copy `.env.example` to `.env` for a fresh setup.
- **Manual Test**: Use `example.txt` request payloads via `POST /api/v1/translate` with header `X-API-Key: <key>`
- **Unit Tests**: `pytest` (dev dependency in `requirements-dev.txt`; install via `pip install -r requirements-dev.txt`). Run `pytest` from `backend/`. Fast tests in `tests/` cover language detection/mapping, cache, preprocessing, quality scoring, transliteration, API-key auth, and the refinement fallback — none load ML models (config env is stubbed in `tests/conftest.py`). Reserve the `integration` marker for model-loading tests. Heavy end-to-end pipeline validation is still manual (see below).

## 🏗 System Architecture & Lifecycles
- **Working Root**: The `backend/` directory is the working root. Sibling `frontend/` is out of scope.
- **Model Loading**: Heavy singletons load eagerly on startup via `app/main.py` `lifespan` before serving.
- **Managers**: `ModelManager` (NLLB), `EmbeddingManager`, `TranslationRefiner`, and `FAISSManager` are lazy-loaded singletons via classmethods. They hold model weights in class attributes. `IndicTrans2Manager` (`app/core/models/indictrans2_manager.py`) is also a singleton but loads **lazily on first Indic→English request** (not eagerly in `lifespan`), so startup stays light and doesn't require the gated IndicTrans2 model unless it's used.
- **Config Loader**: Loaded from `.env` via pydantic-settings (`app/core/config/settings.py`). All fields are strictly required with no defaults. Missing keys will crash startup.
- **Config Keys**: `APP_NAME`, `APP_VERSION`, `DEBUG`, `HOST`, `PORT`, `PROJECT_NAME`, `API_KEY`, `DATABASE_URL`, `TRANSLATION_MODEL`, `EMBEDDING_MODEL`, `REFINEMENT_MODEL`, `INDICTRANS2_INDIC_EN_MODEL`, `RATE_LIMIT`.
- **IndicTrans2 is a gated HF model**: `INDICTRANS2_INDIC_EN_MODEL` (`ai4bharat/indictrans2-indic-en-dist-200M`) requires accepting the license at its HF page and an authenticated token (`huggingface-cli login` or `HF_TOKEN`) to download. Needs the `IndicTransToolkit` dependency. Only the Indic→English path touches it; other routes work without it.

## 🔄 Request Flow (`POST /api/v1/translate`)
1. **Route Orchestrator**: `app/api/routes/translation.py` receives request and verifies the `X-API-Key` dependency.
2. **Async Offloading**: The CPU-bound pipeline is offloaded to a thread pool via `run_inference_async` (`app/utils/async_inference.py`) to keep the main event loop unblocked.
3. **Pipeline Chain (`TranslationPipeline.run()`)**:
   - **Language Detection**: Rule-first Unicode checks for Devanagari/Bengali -> Keyword matches for roman-Hindi -> `langdetect` fallback (0.80 floor). Unknown defaults to `hin_Deva`.
   - **Transliteration**: Converts `roman_hindi` string inputs directly into Devanagari script.
   - **RAG Retrieval**: Vectorizes text using `SentenceTransformers` -> Queries in-memory `IndexFlatL2` FAISS index (Dimension: **384**) linked to a parallel python list `stored_texts` -> Builds context string.
   - **Translation Engine**: Any-to-any via `TranslationRouter` (`app/services/translation/translation_router.py`), which picks the engine per (source, target): **IndicTrans2** (`IndicTrans2Translator`) for Indic→English, **NLLB** (`IndicTranslator`) for everything else. Both expose `translate(text, src_lang, tgt_lang)`. Same-language requests short-circuit (no model). Results cache in `CacheManager` keyed by target code. Target comes from the request's `target_language` (mapped via `LanguageMapper.get_target_code`); unknown targets default to English.
   - **LLM Refinement**: Runs `TranslationRefiner.refine_translation` on the **English translated text** + semantic context string. Falls back to the translated text if the model returns an empty string.
4. **Data Persistence**: Route logs counters via class-level `AnalyticsManager`, saves records to SQLite (`bhashabridge.db`) via SQLAlchemy with `check_same_thread=False`, and appends live data to the FAISS vector space.

## ⚠️ Codebase Quirks & Current Behavior
- **Refinement Ordering**: Refinement runs *after* translation, on the English output. flan-t5 has no Indic vocabulary, so refining pre-translation Devanagari produced whitespace-only output; a fallback returns the translated text if refinement comes back empty.
- **Cache Hit Flag**: `cache_hit` is initialized to `False` before the supported-language block, so unsupported languages no longer crash the response.
- **API Key**: `api_key.py` reads `settings.API_KEY` from the config module.
- **Untranslatable Passthrough**: The pipeline only calls a model when the source is known (`detected_language != "unknown"`) and source code != target code. Otherwise `translated_text` is the (pre)processed input unchanged. Any-to-any direction and Indic→English IndicTrans2 routing are implemented; en→indic / indic→indic IndicTrans2 directions are not yet added (NLLB handles them).

## 📏 Strict Code Style Guardrails
- **Modular Layout**: Keep API routes thin. Business logic and pipeline handling belong strictly in services.
- **Formatting Quirk**: Code style across this repo is unusually sparse. Write exactly **one statement per stanza** with blank lines between almost every single line of code. Match this layout exactly.
- **Logging**: Use `print()` statements alongside the official system logger (`app/core/logging/logger.py`).
- **Rate Limits**: The translate route is hard-capped at `5/minute` via slowapi. `SlowAPIMiddleware` is global.

## 🚫 Token Optimization Exclusions
Claude Code must never index, scan, or read these directories. Add them to your context skip-list:
- `.venv/` | `venv/` | `__pycache__/` | `.git/` | `node_modules/` | `bhashabridge.db` | `*.log`
