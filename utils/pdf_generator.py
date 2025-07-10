from fpdf import FPDF
import os
from datetime import datetime

def export_chat_to_pdf(chat_history, output_dir=".", filename="career_chat.pdf"):
    """
    Export chat history to a PDF file.

    Args:
        chat_history (list): List of chat messages (dicts with "role" and "content").
        output_dir (str): Directory where the PDF will be saved.
        filename (str): Name of the generated PDF file.

    Returns:
        str: Path to the generated PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Career Copilot AI - Chat Transcript", ln=True, align='C')
    pdf.ln(5)

    # Date & Time
    pdf.set_font("Arial", size=10)
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    pdf.cell(0, 10, f"Generated on: {timestamp}", ln=True)
    pdf.ln(5)

    # Chat messages
    pdf.set_font("Arial", size=12)
    for entry in chat_history:
        role = "🧑 User" if entry["role"] == "user" else "🤖 Assistant"
        content = entry["content"].strip()
        pdf.multi_cell(0, 10, f"{role}:\n{content}\n", align='L')
        pdf.ln(1)

    # Save file
    full_path = os.path.join(output_dir, filename)
    pdf.output(full_path)
    return full_path
