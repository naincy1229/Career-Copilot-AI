# utils/parse_resume.py

import fitz  # PyMuPDF

def parse_resume(file):  # expects a file-like object, not a string path
    """Extract plain text from a PDF file object."""
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text
