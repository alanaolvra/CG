import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from Agente.prompt import get_prompt

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4.1-nano",
    openai_api_key=api_key
)

def extrair_dados(frase, tipo_prompt):
    prompt = get_prompt(frase, tipo_prompt)

    resposta = llm.invoke(prompt)
    try:
        return resposta.content
    except:
        print("⚠️ Erro ao interpretar frase!")
        print(resposta.content)
        return None
