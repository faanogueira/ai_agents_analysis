# orchestrator.py — Orquestrador principal do sistema multiagente
import os
import sys
import time
from datetime import datetime

from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva
from agents.ceo_agent import gerar_relatorio_ceo
from agents.sales_agent import gerar_relatorio_vendas

def exibir_cabecalho():
    """Exibe o cabeçalho do sistema."""
    print("\n" + "=" * 60)
    print("  🤖 SISTEMA MULTIAGENTE — SUPERSTORE ANALYTICS")
    print("  Powered by Fábio Nogueira for Google Gemini + Agno Framework")
    print("=" * 60)
    print(f"  Execução iniciada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60 + "\n")

def exibir_progresso(etapa: int, total: int, descricao: str):
    """Exibe o progresso da execução."""
    print(f"\n[{etapa}/{total}] {descricao}")
    print("-" * 40)

def executar_pipeline():
    """
    Executa o pipeline completo do sistema multiagente:
    1. Agente Analista coleta e interpreta os dados
    2. Agente CEO gera relatório estratégico
    3. Agente Vendas gera relatório operacional
    """
    exibir_cabecalho()
    inicio = time.time()
    resultados = {}

    try:
        # ── Etapa 1: Agente Analista ───────────────────────────
        exibir_progresso(1, 4, "Agente Analista — Coletando e processando dados")
        dados = coletar_dados_analiticos()
        resultados["dados"] = dados
        print(f"  ✅ Dados coletados: {len(dados)} dimensões de análise")

        # ── Etapa 2: Análise Executiva ─────────────────────────
        exibir_progresso(2, 4, "Agente Analista — Gerando análise executiva com IA")
        analise = gerar_analise_executiva(dados)
        resultados["analise"] = analise
        print(f"  ✅ Análise gerada: {len(analise.split())} palavras")

        # ── Etapa 3: Agente CEO ────────────────────────────────
        exibir_progresso(3, 4, "Agente CEO — Gerando relatório estratégico executivo")
        relatorio_ceo = gerar_relatorio_ceo(analise, dados)
        resultados["relatorio_ceo"] = relatorio_ceo
        print(f"  ✅ Relatório CEO gerado: {len(relatorio_ceo.split())} palavras")

        # ── Etapa 4: Agente Vendas ─────────────────────────────
        exibir_progresso(4, 4, "Agente Vendas — Gerando relatório operacional")
        relatorio_vendas = gerar_relatorio_vendas(analise, dados)
        resultados["relatorio_vendas"] = relatorio_vendas
        print(f"  ✅ Relatório Vendas gerado: {len(relatorio_vendas.split())} palavras")

    except Exception as e:
        print(f"\n❌ Erro durante a execução: {e}")
        raise

    # ── Resumo Final ───────────────────────────────────────────
    duracao = round(time.time() - inicio, 2)
    print("\n" + "=" * 60)
    print("  ✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    print(f"  ⏱️  Tempo total de execução: {duracao}s")
    print(f"  📁 Relatórios salvos em: reports/")
    print(f"  📄 Arquivos gerados:")

    # Lista os relatórios gerados
    for arquivo in sorted(os.listdir("reports")):
        if arquivo.endswith(".md"):
            caminho = os.path.join("reports", arquivo)
            tamanho = os.path.getsize(caminho)
            print(f"      └─ {arquivo} ({tamanho:,} bytes)")

    print("=" * 60 + "\n")
    return resultados


if __name__ == "__main__":
    executar_pipeline()