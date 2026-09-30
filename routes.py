from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import BASE_DIR
from app.schemas import ComicResponse, PanelResponse, PromptRequest
from app.services.exporters import save_pdf
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image, test_image
from app.services.layout_builder import build_comic_layout

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

def _generate_comic(data):
    outline = generate_outline(
        data.story_prompt, data.character_name, data.setting,
        data.tone, data.art_style
    )
    story = generate_story(
        outline, data.story_prompt, data.character_name, data.setting,
        data.tone, data.art_style
    )
    images = [
        generate_image(panel.image_prompt, panel.panel_number)
        for panel in story.panels
    ]
    layout = build_comic_layout(story, images)
    return layout, save_pdf(layout)

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    data = PromptRequest(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
    )
    try:
        layout, pdf_path = _generate_comic(data)
    except Exception as exc:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": str(exc), "form": data.model_dump()},
            status_code=500,
        )

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={"layout": layout, "pdf_url": "/" + pdf_path},
    )

@router.post("/generate-comic/json", response_model=ComicResponse)
async def generate_comic_json(data: PromptRequest):
    try:
        layout, pdf_path = _generate_comic(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    panels = [
        PanelResponse(
            panel_number=p["panel_number"],
            title=p["title"],
            scene_description=p["scene_description"],
            caption=p["caption"],
            narration=p["narration"],
            dialogue=p["dialogue"],
            image_prompt=p["image_prompt"],
            image_url="/" + p["image_path"],
        )
        for p in layout
    ]
    return ComicResponse(panels=panels, pdf_url="/" + pdf_path)

@router.get("/test-image", response_class=HTMLResponse)
async def test_image_route(request: Request, prompt: str = "A brave fox in an enchanted forest"):
    try:
        image_path = test_image(prompt)
    except Exception as exc:
        return HTMLResponse(f"<h1>Image generation failed</h1><pre>{exc}</pre>", status_code=500)
    return templates.TemplateResponse(
        request=request,
        name="test_image.html",
        context={"image_url": "/" + image_path, "prompt": prompt},
    )

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={"pdf_url": pdf},
    )

@router.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft"}

