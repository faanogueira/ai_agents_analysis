# agents/ceo_agent.py — Agente Redator CEO: gera relatório estratégico executivo
import os
import json
from google import genai
from dotenv import load_dotenv
from tools.report_tools import salvar_relatorio

load_dotenv()

# ── Inicializa cliente Gemini ──────────────────────────────────
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def gerar_relatorio_ceo(analise_executiva: str, dados: dict) -> str:
    """
    Recebe a análise do Agente Analista e gera um relatório
    estratégico formatado para o CEO em Markdown.
    """
    print("👔 Agente CEO: gerando relatório estratégico...")

    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Você é um consultor estratégico sênior preparando um relatório executivo para o CEO da Superstore.

Baseado na análise abaixo, crie um relatório executivo em português, 
profissional e objetivo, focado em decisões estratégicas de alto nível.

ANÁLISE DO ANALISTA:
{analise_executiva}

DADOS BRUTOS:
{dados_json}

O relatório deve seguir EXATAMENTE esta estrutura em Markdown:

# Relatório Executivo — Superstore (2014-2017)
**Classificação:** Confidencial | **Destinatário:** CEO

## Executive Summary
[3-4 parágrafos com os pontos mais críticos para decisão imediata]

## KPIs Estratégicos
[Tabela com os 5 KPIs mais importantes com status: ✅ Saudável / ⚠️ Atenção / 🚨 Crítico]

## Decisões Estratégicas Recomendadas
[3 decisões prioritárias com impacto estimado e prazo sugerido]

## Riscos Identificados
[Top 3 riscos com probabilidade e impacto]

## Oportunidades de Crescimento
[Top 3 oportunidades com potencial de retorno]

## Próximos Passos — 90 dias
[Plano de ação concreto com responsáveis e métricas de sucesso]

Use linguagem executiva, seja direto e foque em impacto financeiro.
Inclua números concretos em todas as recomendações.
"""

    resposta = cliente.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    relatorio = resposta.text
    print("✅ Agente CEO: relatório gerado!")

    # Salva o relatório em arquivo Markdown
    caminho = salvar_relatorio("relatorio_ceo", relatorio)
    print(f"💾 Relatório salvo em: {caminho}")

    return relatorio


if __name__ == "__main__":
    # Testa o agente CEO de forma isolada
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva

    # Coleta dados e gera análise
    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)

    # Gera relatório CEO
    relatorio = gerar_relatorio_ceo(analise, dados)

    print("\n" + "=" * 60)
    print(relatorio)