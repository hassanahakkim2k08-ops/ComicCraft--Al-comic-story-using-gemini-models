import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_story(panels_outline: list, character: str, tone: str) -> list:
    model = genai.GenerativeModel('models/gemini-1.5-pro')
    
    enhanced_panels = []
    for panel in panels_outline:
        prompt = f"""
        Expand this comic panel into story details:
        Panel Title: {panel['title']}
        Description: {panel['description']}
        Main Character: {character}
        Tone: {tone}

        Provide a short narration caption and dynamic dialogue for character '{character}'.
        Format:
        Caption: [Narrative caption]
        Dialogue: [Character dialogue]
        """
        response = model.generate_content(prompt)
        text_output = response.text.strip()
        
        caption, dialogue = "", ""
        for line in text_output.split("\n"):
            if line.startswith("Caption:"):
                caption = line.replace("Caption:", "").strip()
            elif line.startswith("Dialogue:"):
                dialogue = line.replace("Dialogue:", "").strip()

        panel_copy = panel.copy()
        panel_copy["caption"] = caption if caption else text_output
        panel_copy["dialogue"] = dialogue
        enhanced_panels.append(panel_copy)
        
    return enhanced_panels