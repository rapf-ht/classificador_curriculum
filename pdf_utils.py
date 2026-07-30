import pdfplumber
from io import BytesIO

def extract_text_from_pdf(pdf_bytes):
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        text_space = ''
        for page in pdf.pages:
            text_space += page.extract_text() + '\n' # Extraindo texto de cada página
    return text_space.strip()