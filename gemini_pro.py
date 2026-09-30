import json
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY, GEMINI_PRO_MODEL
from app.schemas import ComicOutline, ComicStory

def _client():
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
    return genai.Client(api_key=GEMINI_API_KEY)

def generate_story(outline, story_prompt, character_name, setting, tone, art_style):
    outline_json = json.dumps(outline.model_dump(), ensure_ascii=False, indent=2)
    prompt = f"""
Expand this outline into a polished {len(outline.panels)}-panel comic.

Original idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Outline:
{outline_json}

Requirements:
- Return exactly one StoryPanel for every outline panel.
- Preserve panel order and continuity.
- caption: one short atmospheric caption.
- narration: 1-3 concise sentences.
- dialogue: natural dialogue, or an empty string if none is needed.
- Keep the story suitable for a general audience.
- Keep image_prompt visually focused.
"""
    response = _client().models.generate_content(
        model=GEMINI_PRO_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ComicStory,
            temperature=0.8,
        ),
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty story.")
    return ComicStory.model_validate_json(response.text)

