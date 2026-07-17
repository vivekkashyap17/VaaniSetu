# VaaniSetu — Frontend

React + Vite single-page app for the VaaniSetu translation service. See the
[project README](../README.md) for the full overview.

## Setup

```bash
npm install
cp .env.example .env      # then set the values below
npm run dev               # http://localhost:5173
```

## Environment Variables

| Name | Description |
|------|-------------|
| `VITE_API_BASE_URL` | Base URL of the backend API (e.g. `http://localhost:8000`) |
| `VITE_API_KEY` | `X-API-Key` sent with requests — must match the backend `API_KEY` |

> `VITE_API_KEY` is baked into the browser bundle at build time, so it is
> public by design. Use a low-risk gate key, never a real secret.

## Scripts

- `npm run dev` — start the dev server with HMR
- `npm run build` — production build to `dist/`
- `npm run preview` — preview the production build
