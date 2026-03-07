# agents/analyst_agent.py
import sys
import os

# Adiciona a raiz do projeto ao path do Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# agents/analyst_agent.py — Agente Analista: processa dados e prepara contexto
import json
from google import genai
from dotenv import load_dotenv
from tools.data_tools import (
    obter_resumo_geral,
    vendas_por_categoria,
    vendas_por_regiao,
    top_subcategorias_lucro,
    tendencia_vendas_anual,
    vendas_por_segmento,
    impacto_desconto,
)

load_dotenv()

# ── Inicializa cliente Gemini ──────────────────────────────────
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def coletar_dados_analiticos() -> dict:
    """
    Coleta e organiza todos os dados do dataset.
    Retorna um dicionário estruturado para os agentes redatores.
    """
    print("🔍 Agente Analista: coletando dados...")

    dados = {
        "resumo_geral": obter_resumo_geral(),
        "vendas_por_categoria": vendas_por_categoria(),
        "vendas_por_regiao": vendas_por_regiao(),
        "top_subcategorias": top_subcategorias_lucro(),
        "tendencia_anual": tendencia_vendas_anual(),
        "vendas_por_segmento": vendas_por_segmento(),
        "impacto_desconto": impacto_desconto(),
    }

    print("✅ Agente Analista: dados coletados com sucesso!")
    return dados

def gerar_analise_executiva(dados: dict) -> str:
    """
    Usa o Gemini para interpretar os dados e gerar
    uma análise executiva estruturada em texto.
    """
    print("🤖 Agente Analista: gerando análise executiva com Gemini...")

    # Serializa os dados para enviar ao modelo
    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Você é um analista sênior de dados com experiência em varejo.
Analise os dados abaixo do dataset Superstore (varejo USA 2014-2017)
e gere uma análise executiva estruturada em português.

DADOS:
{dados_json}

Gere uma análise com os seguintes tópicos:
1. **Visão Geral do Negócio** - principais números e período
2. **Performance por Categoria** - destaques e alertas
3. **Análise Regional** - regiões fortes e oportunidades
4. **Tendência de Crescimento** - evolução YoY
5. **Alertas Críticos** - problemas que precisam de atenção imediata
6. **Oportunidades Identificadas** - onde focar para crescer

Seja direto, use números concretos e destaque insights acionáveis.
Formate em Markdown com headers, bullets e tabelas onde adequado.
"""

    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    analise = resposta.text
    print("✅ Agente Analista: análise gerada!")
    return analise


if __name__ == "__main__":
    # Teste isolado do agente analista
    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)
    print("\n" + "=" * 60)
    print(analise)