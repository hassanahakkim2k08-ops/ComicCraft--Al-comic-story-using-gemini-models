import os
import re
import torch
from diffusers import StableDiffusionPipeline

_pipe = None

def get_pipeline():
    global _pipe
    if _pipe is None:
        model_id = "runwayml/stable-diffusion-v1-5"
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        
        _pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=dtype,
            use_safetensors=True
        )
        _pipe.to(device)
    return _pipe

def generate_image(prompt: str, panel_num: int) -> str:
    pipe = get_pipeline()
    
    clean_prompt = re.sub(r'[^a-zA-Z0-9 ]', '', prompt)[:50].replace(" ", "_")
    filename = f"panel_{panel_num}_{clean_prompt}.png"
    filepath = os.path.join("static", "panels", filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    image = pipe(prompt, num_inference_steps=25).images[0]
    image.save(filepath)
    
    return f"/static/panels/{filename}"