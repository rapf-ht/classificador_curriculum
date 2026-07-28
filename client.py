import os
import json
import google.generativeai as genai
from dotenv import load_dotenv # api key call

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Lê o system prompt a partir do gen.md (só a parte antes do "---")
with open("gen.md", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read().split("---")[0].strip()

_model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # test
    system_instruction=SYSTEM_PROMPT,
)


def analisar_curriculo(texto_curriculo: str, texto_vaga: str) -> dict:
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
            "temperature": 0.3, #
        },
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        cleaned = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)