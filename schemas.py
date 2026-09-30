from typing import List
from pydantic import BaseModel, Field

class PanelOutline(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    image_prompt: str

class ComicOutline(BaseModel):
    panels: List[PanelOutline]

class StoryPanel(BaseModel):
    panel_number: int = Field(ge=1, le=5)
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str

class ComicStory(BaseModel):
    panels: List[StoryPanel]

class PromptRequest(BaseModel):
    story_prompt: str = Field(min_length=3, max_length=2000)
    character_name: str = Field(min_length=1, max_length=80)
    setting: str = Field(min_length=1, max_length=120)
    tone: str = Field(min_length=1, max_length=40)
    art_style: str = Field(min_length=1, max_length=80)

class PanelResponse(BaseModel):
    panel_number: int
    title: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str
    image_url: str

class ComicResponse(BaseModel):
    panels: List[PanelResponse]
    pdf_url: str

