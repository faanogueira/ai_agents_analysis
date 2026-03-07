# test_api.py — Valida se a API do Gemini está funcionando
import os
from google import genai
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Inicializa o cliente do Gemini
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def testar_conexao():
    """Envia uma mensagem simples para validar a conexão com a API."""
    
    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents="Responda em português: Você está pronto para analisar dados de vendas do Superstore?"
    )
    
    texto = resposta.text
    print("✅ Conexão com Gemini estabelecida!")
    print(f"Resposta: {texto}")

if __name__ == "__main__":
    testar_conexao()