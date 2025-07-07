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
        dados = json.loads(resposta.content)  
        print(f"🔍 Intenção detectada: {dados['intent']}")  
        return dados['resposta']  
    except Exception as e:
        print("⚠️ Erro ao interpretar a resposta da LLM!")
        print("Resposta bruta:", resposta.content)
        print("Erro:", e)
        return None
