from pathlib import Path
import hashlib
from PIL import Image, ImageDraw, ImageFont

from app.config import (
    HF_TOKEN, IMAGE_GUIDANCE_SCALE, IMAGE_HEIGHT, IMAGE_PROVIDER,
    IMAGE_SEED, IMAGE_STEPS, IMAGE_WIDTH, PANELS_DIR, SD_MODEL_ID
)

_pipeline = None

def _filename(prompt, panel_number):
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:12]
    return f"panel_{panel_number}_{digest}.png"

def _placeholder(prompt, panel_number):
    path = PANELS_DIR / _filename(prompt, panel_number)
    image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), "white")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("arial.ttf", 18)
        title = ImageFont.truetype("arialbd.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
        title = font
    draw.rectangle((10, 10, IMAGE_WIDTH-10, IMAGE_HEIGHT-10), outline="black", width=4)
    draw.text((25, 30), f"ComicCraft - Panel {panel_number}", font=title, fill="black")
    words, lines, line = prompt.split(), [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if len(candidate) > 48:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    y = 100
    for text in lines[:20]:
        draw.text((25, y), text, font=font, fill="black")
        y += 25
    image.save(path)
    return path

def _load_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline

    import torch
    from diffusers import StableDiffusionPipeline

    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    kwargs = {"torch_dtype": dtype, "use_safetensors": True}
    if HF_TOKEN:
        kwargs["token"] = HF_TOKEN

    _pipeline = StableDiffusionPipeline.from_pretrained(SD_MODEL_ID, **kwargs)
    _pipeline = _pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
    _pipeline.enable_attention_slicing()
    return _pipeline

def generate_image(image_prompt, panel_number, negative_prompt=None):
    path = PANELS_DIR / _filename(image_prompt, panel_number)
    if path.exists():
        return path.relative_to(PANELS_DIR.parent.parent).as_posix()

    prompt = (
        f"{image_prompt}. Comic illustration, clear composition, expressive characters, "
        "cohesive visual storytelling, clean line art, cinematic lighting."
    )
    negative = negative_prompt or (
        "blurry, distorted anatomy, extra fingers, duplicate characters, text, watermark, logo"
    )

    if IMAGE_PROVIDER in {"placeholder", "mock"}:
        _placeholder(prompt, panel_number)
    else:
        import torch
        generator = None
        if IMAGE_SEED:
            generator = torch.Generator(
                device="cuda" if torch.cuda.is_available() else "cpu"
            ).manual_seed(int(IMAGE_SEED) + panel_number)

        result = _load_pipeline()(
            prompt=prompt,
            negative_prompt=negative,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT,
            num_inference_steps=IMAGE_STEPS,
            guidance_scale=IMAGE_GUIDANCE_SCALE,
            generator=generator,
        )
        result.images[0].save(path)

    return path.relative_to(PANELS_DIR.parent.parent).as_posix()

def test_image(prompt):
    return generate_image(prompt, 0)

