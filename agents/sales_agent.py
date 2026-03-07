# agents/sales_agent.py -- Agente Redator Vendas: gera relatorio operacional
import os
import json
from google import genai
from dotenv import load_dotenv
from tools.report_tools import salvar_relatorio
from utils.helpers import com_retry, logger

load_dotenv()

# -- Inicializa cliente Gemini
cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def gerar_relatorio_vendas(analise_executiva: str, dados: dict) -> str:
    """Gera relatorio operacional de vendas formatado para o time comercial."""
    logger.info("Agente Vendas: gerando relatorio operacional...")

    dados_json = json.dumps(dados, ensure_ascii=False, indent=2, default=str)

    prompt = f"""
Voce e um gerente senior de vendas preparando um relatorio operacional
para o time comercial da Superstore.

Baseado na analise abaixo, crie um relatorio operacional em portugues,
pratico e orientado a acao, focado em performance regional e por categoria.

ANALISE DO ANALISTA:
{analise_executiva}

DADOS BRUTOS:
{dados_json}

O relatorio deve seguir EXATAMENTE esta estrutura em Markdown:

# Relatorio Operacional de Vendas -- Superstore (2014-2017)
**Destinatario:** Gerencia de Vendas e Time Comercial

## Resumo de Performance
[Visao rapida dos numeros de vendas com comparativo entre periodos]

## Performance Regional Detalhada
[Analise de cada regiao com pontos fortes, fracos e metas sugeridas]

## Analise por Categoria e Sub-Categoria
[Top performers e subcategorias problematicas com recomendacoes taticas]

## Perfil dos Clientes por Segmento
[Analise de Consumer, Corporate e Home Office com estrategias especificas]

## Analise do Impacto de Descontos
[Como os descontos estao afetando as vendas e margem por regiao/categoria]

## Metas e Acoes para o Proximo Trimestre
[Metas SMART por regiao e categoria com responsaveis]

## Ranking de Produtos -- Foco Imediato
[Top 5 produtos para impulsionar e bottom 5 para revisar]

Use linguagem comercial e pratica. Foque em acoes concretas que o
time de vendas pode executar imediatamente. Inclua metas numericas.
"""

    resposta = com_retry(
        lambda: cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
    )

    relatorio = resposta.text
    logger.info("Agente Vendas: relatorio gerado com sucesso!")

    caminho = salvar_relatorio("relatorio_vendas", relatorio)
    logger.info(f"Relatorio Vendas salvo em: {caminho}")

    return relatorio


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva

    dados = coletar_dados_analiticos()
    analise = gerar_analise_executiva(dados)
    relatorio = gerar_relatorio_vendas(analise, dados)

    print("\n" + "=" * 60)
    print(relatorio)
