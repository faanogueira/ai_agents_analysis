# agents/sales_agent.py — Agente Redator Vendas: gera relatório operacional
import os
import json
from google import genai
from dotenv import load_dotenv
from tools.report_tools import salvar_relatorio

load_dotenv()

# ── Inicializa cliente Gemini ──────────────────────────────────
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_relatorio_vendas(analise_executiva: str, dados: dict) -> str:
    """
    Recebe a análise do Agente Analista e gera um relatório
    operacional de vendas formatado para o time comercial.
    """
    print("📈 Agente Vendas: gerando relatório operacional...")

    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Você é um gerente sênior de vendas preparando um relatório operacional
para o time comercial da Superstore.

Baseado na análise abaixo, crie um relatório operacional em português,
prático e orientado a ação, focado em performance regional e por categoria.

ANÁLISE DO ANALISTA:
{analise_executiva}

DADOS BRUTOS:
{dados_json}

O relatório deve seguir EXATAMENTE esta estrutura em Markdown:

# Relatório Operacional de Vendas — Superstore (2014-2017)
**Destinatário:** Gerência de Vendas e Time Comercial

## Resumo de Performance
[Visão rápida dos números de vendas com comparativo entre períodos]

## Performance Regional Detalhada
[Análise de cada região com pontos fortes, fracos e metas sugeridas]

## Análise por Categoria e Sub-Categoria
[Top performers e subcategorias problemáticas com recomendações táticas]

## Perfil dos Clientes por Segmento
[Análise de Consumer, Corporate e Home Office com estratégias específicas]

## Análise do Impacto de Descontos
[Como os descontos estão afetando as vendas e margem por região/categoria]

## Metas e Ações para o Próximo Trimestre
[Metas SMART por região e categoria com responsáveis]

## Ranking de Produtos — Foco Imediato
[Top 5 produtos para impulsionar e bottom 5 para revisar]

Use linguagem comercial e prática. Foque em ações concretas que o
time de vendas pode executar imediatamente. Inclua metas numéricas.
"""

    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    relatorio = resposta.text
    print("✅ Agente Vendas: relatório gerado!")

    # Salva o relatório em arquivo Markdown
    caminho = salvar_relatorio("relatorio_vendas", relatorio)
    print(f"💾 Relatório salvo em: {caminho}")

    return relatorio


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva

    # Coleta dados e gera análise
    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)

    # Gera relatório de Vendas
    relatorio = gerar_relatorio_vendas(analise, dados)

    print("\n" + "=" * 60)
    print(relatorio)