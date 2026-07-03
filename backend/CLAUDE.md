# CLAUDE.md - BhashaBridge

System architecture blueprint and token-saving caching guardrails for Claude Code.

## 🛠 Development Workflow Commands
- **Install Deps**: `pip install -r requirements.txt` (Run from `backend/` inside active `.venv`)
- **Run API**: `uvicorn app.main:app --reload`
- **Manual Test**: Use `example.txt` request payloads via `POST /api/v1/translate` with header `X-API-Key: <key>`
- **Framework**: No formal testing framework (e.g., pytest) is configured. All validation is manual.

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
   - **LLM Refinement**: Runs `TranslationRefiner.refine_translation` using original text + semantic context string.
   - **Translation Engine**: Supported languages hit `CacheManager` dict or process via `IndicTranslator` (Target code is always English `eng_Latn`).
4. **Data Persistence**: Route logs counters via class-level `AnalyticsManager`, saves records to SQLite (`bhashabridge.db`) via SQLAlchemy with `check_same_thread=False`, and appends live data to the FAISS vector space.

## ⚠️ Known Codebase Bugs & Quirks
- **Refinement Ordering**: In `TranslationPipeline.run()`, step 3 (Refinement) deliberately runs *before* step 4 (Translation). Refinement processes raw pre-translation text. Do not reverse this sequence.
- **Unbound Cache Variable**: The `cache_hit` variable is only set within the supported-language block. If an unsupported language hits the route, `cache_hit` is unbound and crashes the service response.
- **Missing Imports**: `api_key.py` references an undefined global variable `API_KEY` instead of importing and reading `settings.API_KEY`. Fix this using the config module.

## 📏 Strict Code Style Guardrails
- **Modular Layout**: Keep API routes thin. Business logic and pipeline handling belong strictly in services.
- **Formatting Quirk**: Code style across this repo is unusually sparse. Write exactly **one statement per stanza** with blank lines between almost every single line of code. Match this layout exactly.
- **Logging**: Use `print()` statements alongside the official system logger (`app/core/logging/logger.py`).
- **Rate Limits**: The translate route is hard-capped at `5/minute` via slowapi. `SlowAPIMiddleware` is global.

## 🚫 Token Optimization Exclusions
Claude Code must never index, scan, or read these directories. Add them to your context skip-list:
- `.venv/` | `venv/` | `__pycache__/` | `.git/` | `node_modules/` | `bhashabridge.db` | `*.log`
