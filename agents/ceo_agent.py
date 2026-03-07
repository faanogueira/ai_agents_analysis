# agents/ceo_agent.py -- Agente Redator CEO: gera relatorio estrategico executivo
import os
import json
from google import genai
from dotenv import load_dotenv
from tools.report_tools import salvar_relatorio
from utils.helpers import com_retry, logger

load_dotenv()

# -- Inicializa cliente Gemini
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gerar_relatorio_ceo(analise_executiva: str, dados: dict) -> str:
    """Gera relatorio estrategico formatado para o CEO em Markdown."""
    logger.info("Agente CEO: gerando relatorio estrategico...")

    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Voce e um consultor estrategico senior preparando um relatorio executivo para o CEO da Superstore.

Baseado na analise abaixo, crie um relatorio executivo em portugues,
profissional e objetivo, focado em decisoes estrategicas de alto nivel.

ANALISE DO ANALISTA:
{analise_executiva}

DADOS BRUTOS:
{dados_json}

O relatorio deve seguir EXATAMENTE esta estrutura em Markdown:

# Relatorio Executivo -- Superstore (2014-2017)
**Classificacao:** Confidencial | **Destinatario:** CEO

## Executive Summary
[3-4 paragrafos com os pontos mais criticos para decisao imediata]

## KPIs Estrategicos
[Tabela com os 5 KPIs mais importantes com status: OK Saudavel / ATENCAO / CRITICO]

## Decisoes Estrategicas Recomendadas
[3 decisoes prioritarias com impacto estimado e prazo sugerido]

## Riscos Identificados
[Top 3 riscos com probabilidade e impacto]

## Oportunidades de Crescimento
[Top 3 oportunidades com potencial de retorno]

## Proximos Passos -- 90 dias
[Plano de acao concreto com responsaveis e metricas de sucesso]

Use linguagem executiva, seja direto e foque em impacto financeiro.
Inclua numeros concretos em todas as recomendacoes.
"""

    resposta = com_retry(
        lambda: cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    relatorio = resposta.text
    logger.info("Agente CEO: relatorio gerado com sucesso!")

    caminho = salvar_relatorio("relatorio_ceo", relatorio)
    logger.info(f"Relatorio CEO salvo em: {caminho}")

    return relatorio


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva

    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)
    relatorio = gerar_relatorio_ceo(analise, dados)

    print("\n" + "=" * 60)
    print(relatorio)
