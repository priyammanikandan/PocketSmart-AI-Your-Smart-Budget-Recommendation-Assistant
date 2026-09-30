from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_FLASH_MODEL, MAX_PANELS
from app.schemas import ComicOutline

def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_outline(story_prompt, character_name, setting, tone, art_style):
    prompt = f"""
Create a cohesive {MAX_PANELS}-panel comic outline.

Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Requirements:
- Return exactly {MAX_PANELS} panels.
- Keep the character and setting visually consistent.
- Give every panel a short title.
- scene_description explains what is visually happening.
- image_prompt must be detailed enough for Stable Diffusion.
- Do not place long written text, logos or watermarks in the artwork.
- Create a clear beginning, middle and ending.
"""
    response = _client().models.generate_content(
        model=GEMINI_FLASH_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicOutline,
            temperature=0.9,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty outline.")
    return ComicOutline.model_validate_json(response.text)

