import os
import json
import google.generativeai as genai
from dotenv import load_dotenv # api key call
from pydantic import BaseModel, Field

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Lê o gen.md e extrai o prompt
# Melhorar isso
with open("gen.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().split("---")[0].strip() # antes do "---"

class AnalysisResult(BaseModel):
    score: int = Field("Nota de 0 a 100, de acordo com a compatibilidade entre a oferta de trabalho e o currículo recebido.")
    job_apply: bool = Field("O candidato está apto para a oferta de trabalho? (true/false)")
    strong_points: list[str] = Field("Pontos fortes do candidato em relação à vaga.")
    weak_points: list[str] = Field("Pontos fracos do candidato em relação à vaga.")
    help_if_needed: str = Field("""
        Recomendações de no máximo 3 linhas, onde o usuário poderia melhorar com relação ao currículo e a vaga, para se destacar. 
        Dando ideias até mesmo de projetos pessoais e/ou cursos que poderiam ajudá-lo a se destacar na vaga.
        Se caso o candidato já esteja apto para a vaga, apenas diga "Nenhuma recomendação adicional.".
        """)
    
_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # test
    system_instruction=SYSTEM_PROMPT,
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

    response = _model.generate_content(
        user_prompt,
        generation_config={
            "response_mime_type": "application/json",
            "temperature": 0.3, # test
        },
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)