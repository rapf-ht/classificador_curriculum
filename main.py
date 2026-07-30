from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pdf_utils import extrair_texto_pdf
from client import analisar_curriculo

app = FastAPI()

# Necessário pro React (rodando em outra porta) conseguir chamar essa API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, trocar "*" pelo domínio do seu front
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.post("/analisar")
async def analisar(
    curriculo: UploadFile = File(...),
    vaga: str = Form(...),
):
    if curriculo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo precisa ser um PDF.")

    conteudo = await curriculo.read()

    try:
        texto_curriculo = extrair_texto_pdf(conteudo)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if not vaga.strip():
        raise HTTPException(status_code=400, detail="A descrição da vaga não pode estar vazia.")

    try:
        resultado = analisar_curriculo(texto_curriculo, vaga)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Erro ao consultar a IA: {str(e)}")

    return resultado