import os

BASE_PROMPT_DIR = os.path.dirname(__file__)

def get_prompt(dto, tipo_prompt="vendedor"):
    prompt_filename = f"prompt_{tipo_prompt}.txt"
    prompt_path = os.path.join(BASE_PROMPT_DIR, "prompts", prompt_filename)

    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt não encontrado: {prompt_filename}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        base_prompt = f.read()

    return base_prompt.replace("{{frase}}", dto)
