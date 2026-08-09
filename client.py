import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv # api key call
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Lê o gen.md e extrai o prompt
# Melhorar isso
with open("gen.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().split("---")[0].strip() # antes do "---"

class AnalysisResult(BaseModel):
    score: int = Field(description="Nota de 0 a 100, de acordo com a compatibilidade entre a oferta de trabalho e o currículo recebido.")
    job_apply: bool = Field(description="O candidato está apto para a oferta de trabalho? (true/false)")
    strong_points: list[str] = Field(description="Pontos fortes do candidato em relação à vaga.")
    weak_points: list[str] = Field(description="Pontos fracos do candidato em relação à vaga.")
    help_if_needed: str = Field(description="""
        Recomendações de no máximo 3 linhas, onde o usuário poderia melhorar com relação ao currículo e a vaga, para se destacar. 
        Dando ideias até mesmo de projetos pessoais e/ou cursos que poderiam ajudá-lo a se destacar na vaga.
        Se caso o candidato já esteja apto para a vaga, apenas diga "Nenhuma recomendação adicional.".
        """)
    
# Reinicia o processo em caso de erro por parte do Google
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    retry=retry_if_exception_type(ServerError),
)

def analisar_curriculo(texto_curriculo: str, texto_vaga: str) -> AnalysisResult:
    user_prompt = f"""
CURRÍCULO:
\"\"\"
{texto_curriculo}
\"\"\"

DESCRIÇÃO DA VAGA:
\"\"\"
{texto_vaga}
\"\"\"

Analise a aderência entre o currículo e a vaga acima, seguindo o formato JSON especificado.
"""

    response = client.models.generate_content(
        model='gemini-3.5-flash-lite',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
            # These two lines guarantee valid JSON matching your Pydantic schema
            response_mime_type="application/json",
            response_schema=AnalysisResult,
        ),
    )

    return response.parsed

# client.file.delete("gen.md") # test/deletar informações sensíveis