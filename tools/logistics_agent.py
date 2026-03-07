# agents/logistics_agent.py — Agente Logística: análise ABC, shipping e margens
import os
import json
from google import genai
from dotenv import load_dotenv
from tools.report_tools import salvar_relatorio
from tools.data_tools import (
    analise_abc_produtos,
    analise_shipping,
    margem_por_produto,
)

load_dotenv()

# ── Inicializa cliente Gemini ──────────────────────────────────
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def coletar_dados_logistica() -> dict:
    """
    Coleta dados específicos de logística e gestão de estoque.
    """
    print("🚚 Agente Logística: coletando dados...")

    dados = {
        "analise_abc": analise_abc_produtos(top_n=10),
        "analise_shipping": analise_shipping(),
        "margem_por_produto": margem_por_produto(bottom_n=10),
    }

    print("✅ Agente Logística: dados coletados!")
    return dados

def gerar_relatorio_logistica(analise_executiva: str, dados_logistica: dict) -> str:
    """
    Gera relatório de logística com foco em estoque,
    shipping e análise ABC de produtos.
    """
    print("🚚 Agente Logística: gerando relatório...")

    dados_json = json.dumps(
        dados_logistica, ensure_ascii=False, indent=2, default=str
    )

    prompt = f"""
Você é um especialista em logística e supply chain preparando um relatório
operacional para o gestor de logística da Superstore.

Baseado nos dados abaixo, crie um relatório técnico em português,
focado em otimização de estoque, shipping e gestão de produtos.

CONTEXTO GERAL DO NEGÓCIO:
{analise_executiva}

DADOS DE LOGÍSTICA:
{dados_json}

O relatório deve seguir EXATAMENTE esta estrutura em Markdown:

# Relatório de Logística e Supply Chain — Superstore (2014-2017)
**Destinatário:** Gerência de Logística e Supply Chain

## Resumo Executivo de Logística
[Principais números de shipping e estoque em 3 parágrafos]

## Análise ABC de Produtos
[Classificação e estratégia para cada classe com tabela resumo]
- Classe A: produtos prioritários (80% da receita)
- Classe B: produtos de suporte (15% da receita)
- Classe C: produtos de cauda longa (5% da receita)

## Performance de Shipping por Modalidade
[Tabela com tempo médio, volume e margem por modalidade de envio]

## Análise de Shipping por Região
[Quais regiões têm melhor e pior performance de entrega]

## Produtos com Margem Crítica
[Top 10 produtos gerando prejuízo com recomendação de ação]

## Recomendações de Otimização de Estoque
[3 ações concretas para reduzir custos e aumentar giro]

## KPIs de Logística — Metas para Próximo Trimestre
[5 KPIs específicos de logística com valores atuais e metas]

Use linguagem técnica de supply chain. Inclua números precisos
e recomendações baseadas em dados. Foque em redução de custos
e melhoria de eficiência operacional.
"""

    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    relatorio = resposta.text
    print("✅ Agente Logística: relatório gerado!")

    # Salva o relatório
    caminho = salvar_relatorio("relatorio_logistica", relatorio)
    print(f"💾 Relatório salvo em: {caminho}")

    return relatorio


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva

    dados_gerais = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados_gerais)
    dados_logistica = coletar_dados_logistica()
    relatorio = gerar_relatorio_logistica(analise, dados_logistica)

    print("\n" + "=" * 60)
    print(relatorio)