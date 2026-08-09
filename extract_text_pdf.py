import pdfplumber
from io import BytesIO


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    texto = ""
    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for pagina in pdf.pages:
            texto_pagina = pagina.extract_text()
            if texto_pagina:
                texto += texto_pagina + "\n"

    if not texto.strip():
        raise ValueError("Não foi possível extrair texto do PDF (pode ser um PDF escaneado/imagem).")

    return texto.strip()