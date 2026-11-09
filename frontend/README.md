# SiliconCrew frontend

Next.js workbench for the SiliconCrew RTL demo.

## Run locally

Start the backend from the repository root:

```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

Then, in another terminal:

```bash
cd frontend
npm ci
npm run dev
```

Open <http://localhost:3000>. The frontend uses `http://localhost:8000` for the backend by default. Set `API_URL` and `WS_URL` only if you are running the backend elsewhere.

## Checks

```bash
npm test
npx tsc --noEmit
```
