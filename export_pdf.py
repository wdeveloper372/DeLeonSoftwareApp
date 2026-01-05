from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from datetime import datetime
import re
import os

def generate_pdf(client_name, results, labor, calibration):
    # Sanitize filename to prevent errors with special characters
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', client_name.replace(' ', '_'))
    if not safe_name: safe_name = "Client"
    
    # Create a 'PDFs' folder if it doesn't exist
    output_folder = "PDFs"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    filename = f"Estimate_{safe_name}_{datetime.now().strftime('%Y%m%d')}.pdf"
    full_path = os.path.join(output_folder, filename)
    
    c = canvas.Canvas(full_path, pagesize=LETTER)
    width, height = LETTER

    # --- Header ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "DE LEON AUTO GLASS")
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 65, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    c.line(50, height - 75, 550, height - 75)

    # --- Client Info ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 100, f"Estimate for: {client_name}")

    # --- Table Layout ---
    c.setFont("Helvetica", 11)
    y_position = height - 140
    
    # Helper to ensure currency format
    def fmt(val):
        try:
            return f"${float(val):.2f}"
        except (ValueError, TypeError):
            return "$0.00"

    items = [
        ("Parts & Profit", fmt(results['parts_profit'])),
        ("Tax", fmt(results['tax'])),
        ("Kit/Materials", fmt(results['kit'])),
        ("Labor", fmt(labor)),
        ("Calibration", fmt(calibration)),
    ]

    for item, price in items:
        c.drawString(50, y_position, item)
        c.drawRightString(200, y_position, price)
        y_position -= 20

    # --- Grand Total ---
    c.line(50, y_position, 200, y_position)
    y_position -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y_position, "GRAND TOTAL:")
    c.drawRightString(200, y_position, fmt(results['total']))

    c.save()
    return full_path