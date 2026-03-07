# listar_modelos.py — Lista todos os modelos disponíveis na sua conta
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Lista todos os modelos disponíveis
for modelo in cliente.models.list():
    print(modelo.name)