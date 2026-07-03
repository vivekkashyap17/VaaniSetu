# CLAUDE.md - BhashaBridge

System architecture blueprint and token-saving caching guardrails for Claude Code.

## 🛠 Development Workflow Commands
- **Install Deps**: `pip install -r requirements.txt` (Run from `backend/` inside active `.venv`)
- **Run API**: `uvicorn app.main:app --reload`
- **Manual Test**: Use `example.txt` request payloads via `POST /api/v1/translate` with header `X-API-Key: <key>`
- **Unit Tests**: `pytest` (dev dependency in `requirements-dev.txt`; install via `pip install -r requirements-dev.txt`). Run `pytest` from `backend/`. Fast tests in `tests/` cover language detection/mapping, cache, preprocessing, quality scoring, transliteration, API-key auth, and the refinement fallback — none load ML models (config env is stubbed in `tests/conftest.py`). Reserve the `integration` marker for model-loading tests. Heavy end-to-end pipeline validation is still manual (see below).

## 🏗 System Architecture & Lifecycles
- **Working Root**: The `backend/` directory is the working root. Sibling `frontend/` is out of scope.
- **Model Loading**: Heavy singletons load eagerly on startup via `app/main.py` `lifespan` before serving.
- **Managers**: `ModelManager`, `EmbeddingManager`, `TranslationRefiner`, and `FAISSManager` are lazy-loaded singletons via classmethods. They hold model weights in class attributes.
- **Config Loader**: Loaded from `.env` via pydantic-settings (`app/core/config/settings.py`). All fields are strictly required with no defaults. Missing keys will crash startup.
- **Config Keys**: `APP_NAME`, `APP_VERSION`, `DEBUG`, `HOST`, `PORT`, `PROJECT_NAME`, `API_KEY`, `DATABASE_URL`, `TRANSLATION_MODEL`, `EMBEDDING_MODEL`, `REFINEMENT_MODEL`, `RATE_LIMIT`.

## 🔄 Request Flow (`POST /api/v1/translate`)
1. **Route Orchestrator**: `app/api/routes/translation.py` receives request and verifies the `X-API-Key` dependency.
2. **Async Offloading**: The CPU-bound pipeline is offloaded to a thread pool via `run_inference_async` (`app/utils/async_inference.py`) to keep the main event loop unblocked.
3. **Pipeline Chain (`TranslationPipeline.run()`)**:
   - **Language Detection**: Rule-first Unicode checks for Devanagari/Bengali -> Keyword matches for roman-Hindi -> `langdetect` fallback (0.80 floor). Unknown defaults to `hin_Deva`.
   - **Transliteration**: Converts `roman_hindi` string inputs directly into Devanagari script.
   - **RAG Retrieval**: Vectorizes text using `SentenceTransformers` -> Queries in-memory `IndexFlatL2` FAISS index (Dimension: **384**) linked to a parallel python list `stored_texts` -> Builds context string.
   - **Translation Engine**: Supported languages hit `CacheManager` dict or process via `IndicTranslator` (Target code is always English `eng_Latn`).
   - **LLM Refinement**: Runs `TranslationRefiner.refine_translation` on the **English translated text** + semantic context string. Falls back to the translated text if the model returns an empty string.
4. **Data Persistence**: Route logs counters via class-level `AnalyticsManager`, saves records to SQLite (`bhashabridge.db`) via SQLAlchemy with `check_same_thread=False`, and appends live data to the FAISS vector space.

## ⚠️ Codebase Quirks & Current Behavior
- **Refinement Ordering**: Refinement runs *after* translation, on the English output. flan-t5 has no Indic vocabulary, so refining pre-translation Devanagari produced whitespace-only output; a fallback returns the translated text if refinement comes back empty.
- **Cache Hit Flag**: `cache_hit` is initialized to `False` before the supported-language block, so unsupported languages no longer crash the response.
- **API Key**: `api_key.py` reads `settings.API_KEY` from the config module.
- **Unsupported Languages**: If `detected_language` is not in the supported set, `translated_text` is returned untranslated (passthrough). Target is always English — any-to-any direction and IndicTrans2 routing are planned, not yet implemented.

## 📏 Strict Code Style Guardrails
- **Modular Layout**: Keep API routes thin. Business logic and pipeline handling belong strictly in services.
- **Formatting Quirk**: Code style across this repo is unusually sparse. Write exactly **one statement per stanza** with blank lines between almost every single line of code. Match this layout exactly.
- **Logging**: Use `print()` statements alongside the official system logger (`app/core/logging/logger.py`).
- **Rate Limits**: The translate route is hard-capped at `5/minute` via slowapi. `SlowAPIMiddleware` is global.

## 🚫 Token Optimization Exclusions
Claude Code must never index, scan, or read these directories. Add them to your context skip-list:
- `.venv/` | `venv/` | `__pycache__/` | `.git/` | `node_modules/` | `bhashabridge.db` | `*.log`
