import os
import time
from fpdf import FPDF

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'ComicCraft AI Generation', 0, 1, 'C')
        self.ln(5)

def save_pdf(layout: list) -> str:
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    for panel in layout:
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True)
        
        img_rel_path = panel['image_path'].lstrip('/')
        if os.path.exists(img_rel_path):
            pdf.image(img_rel_path, x=15, w=180)
            pdf.ln(5)
            
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, f"Scene: {panel['description']}")
        pdf.ln(2)
        
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, f"Caption: {panel['caption']}")
        if panel['dialogue']:
            pdf.set_font("Arial", "B", 10)
            pdf.multi_cell(0, 6, f"Dialogue: {panel['dialogue']}")
            
    timestamp = int(time.time())
    output_filename = f"comic_{timestamp}.pdf"
    output_dir = os.path.join("static", "exports")
    os.makedirs(output_dir, exist_ok=True)
    
    full_path = os.path.join(output_dir, output_filename)
    pdf.output(full_path)
    
    return f"/static/exports/{output_filename}"