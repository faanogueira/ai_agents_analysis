# agents/analyst_agent.py -- Agente Analista: processa dados e prepara contexto
import os
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
from utils.helpers import com_retry, logger

load_dotenv()

# -- Inicializa cliente Gemini
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def coletar_dados_analiticos() -> dict:
    """Coleta e organiza todos os dados do dataset."""
    logger.info("Agente Analista: coletando dados...")

    dados = {
        "resumo_geral": obter_resumo_geral(),
        "vendas_por_categoria": vendas_por_categoria(),
        "vendas_por_regiao": vendas_por_regiao(),
        "top_subcategorias": top_subcategorias_lucro(),
        "tendencia_anual": tendencia_vendas_anual(),
        "vendas_por_segmento": vendas_por_segmento(),
        "impacto_desconto": impacto_desconto(),
    }

    logger.info("Agente Analista: dados coletados com sucesso!")
    return dados


def gerar_analise_executiva(dados: dict) -> str:
    """Usa o Gemini para interpretar os dados e gerar analise executiva."""
    logger.info("Agente Analista: gerando analise executiva com Gemini...")

    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Voce e um analista senior de dados com experiencia em varejo.
Analise os dados abaixo do dataset Superstore (varejo USA 2014-2017)
e gere uma analise executiva estruturada em portugues.

DADOS:
{dados_json}

Gere uma analise com os seguintes topicos:
1. **Visao Geral do Negocio** - principais numeros e periodo
2. **Performance por Categoria** - destaques e alertas
3. **Analise Regional** - regioes fortes e oportunidades
4. **Tendencia de Crescimento** - evolucao YoY
5. **Alertas Criticos** - problemas que precisam de atencao imediata
6. **Oportunidades Identificadas** - onde focar para crescer

Seja direto, use numeros concretos e destaque insights acionaveis.
Formate em Markdown com headers, bullets e tabelas onde adequado.
"""

    resposta = com_retry(
        lambda: cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    analise = resposta.text
    logger.info("Agente Analista: analise executiva gerada com sucesso!")
    return analise


if __name__ == "__main__":
    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)
    print("\n" + "=" * 60)
    print(analise)
