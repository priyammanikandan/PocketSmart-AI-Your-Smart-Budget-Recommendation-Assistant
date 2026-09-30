from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

STATIC_DIR = BASE_DIR / "static"
PANELS_DIR = STATIC_DIR / "panels"
EXPORTS_DIR = STATIC_DIR / "exports"

PANELS_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_FLASH_MODEL = os.getenv("GEMINI_FLASH_MODEL", "gemini-3.8-flash").strip()
GEMINI_PRO_MODEL = os.getenv("GEMINI_PRO_MODEL", "gemini-3.1-pro-preview").strip()

IMAGE_PROVIDER = os.getenv("IMAGE_PROVIDER", "diffusers").strip().lower()
SD_MODEL_ID = os.getenv(
    "SD_MODEL_ID",
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
).strip()
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()

IMAGE_WIDTH = int(os.getenv("IMAGE_WIDTH", "512"))
IMAGE_HEIGHT = int(os.getenv("IMAGE_HEIGHT", "512"))
IMAGE_STEPS = int(os.getenv("IMAGE_STEPS", "20"))
IMAGE_GUIDANCE_SCALE = float(os.getenv("IMAGE_GUIDANCE_SCALE", "7.5"))
IMAGE_SEED = os.getenv("IMAGE_SEED", "").strip()
MAX_PANELS = int(os.getenv("MAX_PANELS", "5"))

