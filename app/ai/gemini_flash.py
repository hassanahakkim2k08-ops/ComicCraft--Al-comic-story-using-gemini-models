import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_outline(prompt: str, character: str, setting: str, tone: str, art_style: str) -> list:
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    system_prompt = f"""
    Create a structured 5-panel comic outline based on:
    Prompt: {prompt}
    Character: {character}
    Setting: {setting}
    Tone: {tone}
    Art Style: {art_style}

    Return strictly a JSON array of 5 objects containing:
    "panel": panel number (1-5),
    "title": concise panel title,
    "description": scene environment description,
    "image_prompt": precise visual prompt for image generator in {art_style} style.
    Do not include markdown or extra text.
    """
    
    response = model.generate_content(system_prompt)
    clean_json = response.text.strip().replace("```json", "").replace("```", "")
    return json.loads(clean_json)