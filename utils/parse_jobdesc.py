def extract_text_from_txt(file):
    """Extract text from a TXT file object."""
    return file.read().decode("utf-8")
