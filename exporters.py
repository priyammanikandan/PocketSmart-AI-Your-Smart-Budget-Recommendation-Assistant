from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from app.config import EXPORTS_DIR, STATIC_DIR

def save_pdf(layout):
    filename = f"comiccraft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    output = EXPORTS_DIR / filename

    pdf = FPDF("P", "mm", "A4")
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, f"Panel {panel['panel_number']}: {panel['title']}", ln=True)

        image_path = (STATIC_DIR.parent / panel["image_path"]).resolve()
        if image_path.exists():
            pdf.image(str(image_path), x=15, y=28, w=180)

        pdf.ln(105)
        pdf.set_font("Helvetica", "I", 10)
        pdf.multi_cell(0, 6, panel["scene_description"])
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.multi_cell(0, 6, f"Caption: {panel['caption']}")
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, f"Narration: {panel['narration']}")
        if panel["dialogue"].strip():
            pdf.multi_cell(0, 6, f"Dialogue: {panel['dialogue']}")

    pdf.output(str(output))
    return f"static/exports/{filename}"

