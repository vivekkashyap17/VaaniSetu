# Deploying VaaniSetu

**Backend** → Hugging Face Space (Docker, free CPU tier).
**Frontend** → Vercel (free).

---

## 1. Backend on Hugging Face Spaces

### 1a. Create a WRITE token (one time)
1. Go to https://huggingface.co/settings/tokens
2. **New token** → Type: **Write** → name it e.g. `vaanisetu-deploy` → **Create**.
3. Copy the `hf_...` value.
4. Make sure you've accepted the IndicTrans2 license once at
   https://huggingface.co/ai4bharat/indictrans2-indic-en-dist-200M (needed so
   the Space can download the gated model).

### 1b. Deploy (run from `backend/`, inside the venv)
```bash
export HF_WRITE_TOKEN=hf_xxx_your_write_token
export APP_API_KEY=<your-api-key>              # the X-API-Key clients must send
export ALLOWED_ORIGINS="*"                     # tighten to your Vercel URL later
python deploy/deploy_hf_space.py
```
This creates `https://huggingface.co/spaces/<you>/vaanisetu-backend`, sets all
config as Space variables/secrets, and uploads the code. The Space then builds
(~a few minutes) and the app is served at:
```
https://<you>-vaanisetu-backend.hf.space
```
Check health: `GET https://<you>-vaanisetu-backend.hf.space/api/v1/health`

> Free CPU tier: the first request after idle is slow while ~5 GB of models
> load. Re-run the script anytime to push updates.

---

## 2. Frontend on Vercel

1. https://vercel.com → **Add New… → Project** → import the `VaaniSetu` repo.
2. **Root Directory**: `frontend`  (Framework preset auto-detects **Vite**).
3. **Environment Variables**:
   | Name | Value |
   |------|-------|
   | `VITE_API_BASE_URL` | `https://<you>-vaanisetu-backend.hf.space` |
   | `VITE_API_KEY` | `<your-api-key>` (same value as `APP_API_KEY` above) |
4. **Deploy**. Vercel gives you a URL like `https://vaanisetu.vercel.app`.

### 2a. (Optional) Lock CORS to your Vercel URL
Once you have the Vercel URL, re-run the backend deploy with it so the API only
accepts your frontend:
```bash
export ALLOWED_ORIGINS="https://vaanisetu.vercel.app"
python deploy/deploy_hf_space.py
```
(Or edit `ALLOWED_ORIGINS` directly in the Space's **Settings → Variables**.)

---

## Notes
- The SPA sends `VITE_API_KEY` from the browser, so it is inherently public —
  this app's `X-API-Key` is a light gate/rate-limit key, not a real secret.
- SQLite (`vaanisetu.db`) and the FAISS index are ephemeral on the free tier
  (reset on Space restart). Fine for a demo.
- `RATE_LIMIT` is set to `30/minute` on the Space (vs `5/minute` locally) for
  smoother testing.
