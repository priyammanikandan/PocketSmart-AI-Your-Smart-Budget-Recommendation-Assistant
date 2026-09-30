# ComicCraft - AI Comic Story Creator

A complete FastAPI application based on the supplied ComicCraft specification.

## Features
- Five-panel comic outline with Gemini structured output
- Detailed narration and dialogue with Gemini
- Stable Diffusion illustrations through Hugging Face Diffusers
- Jinja2 web UI
- JSON API
- PDF export with fpdf2
- Health endpoint and basic tests

## Setup

Use Python 3.11 or 3.12.

### Windows PowerShell
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

If activation is blocked:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\Activate.ps1
```

### macOS/Linux
```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and add:
```text
GEMINI_API_KEY=your_key_here
```

For a fast first test without downloading Stable Diffusion:
```text
IMAGE_PROVIDER=placeholder
```

For real AI images:
```text
IMAGE_PROVIDER=diffusers
```

Then run:
```bash
python -m uvicorn app.main:app --reload
```

Open:
- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/health

Test:
```bash
pytest -q
```

## JSON API
POST `/generate-comic/json`:
```json
{
  "story_prompt": "A young fox discovers a glowing doorway in an enchanted forest.",
  "character_name": "Luna",
  "setting": "Forest",
  "tone": "Adventure",
  "art_style": "Comic book"
}
```

## Important
The original document uses Gemini 1.5 Flash/Pro and `runwayml/stable-diffusion-v1-5`. This implementation preserves the requested architecture but makes model IDs configurable and defaults to currently documented Gemini IDs plus the current Stable Diffusion v1.5 repository, so an obsolete endpoint is not hard-coded.
