from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from .gemini_flash import generate_outline
from .gemini_pro import generate_story
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class PromptRequest(BaseModel):
    prompt: str
    character: str
    setting: str
    tone: str
    art_style: str

@router.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate_comic_form(
    request: Request,
    prompt: str = Form(...),
    character: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...)
):
    try:
        outlines = generate_outline(prompt, character, setting, tone, art_style)
        story_panels = generate_story(outlines, character, tone)
        
        image_paths = []
        for panel in story_panels:
            path = generate_image(panel['image_prompt'], panel['panel'])
            image_paths.append(path)
            
        layout = build_comic_layout(story_panels, image_paths)
        pdf_path = save_pdf(layout)
        
        return templates.TemplateResponse("comic_preview.html", {
            "request": request, 
            "layout": layout, 
            "pdf_path": pdf_path
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        outlines = generate_outline(payload.prompt, payload.character, payload.setting, payload.tone, payload.art_style)
        story_panels = generate_story(outlines, payload.character, payload.tone)
        
        image_paths = [generate_image(p['image_prompt'], p['panel']) for p in story_panels]
        layout = build_comic_layout(story_panels, image_paths)
        pdf_path = save_pdf(layout)
        
        return JSONResponse(content={"layout": layout, "pdf_path": pdf_path})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse("export_success.html", {"request": request, "pdf_path": pdf_path})

@router.post("/test-image")
async def test_image(prompt: str = Form(...)):
    img_path = generate_image(prompt, 99)
    return {"image_path": img_path}