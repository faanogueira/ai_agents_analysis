# orchestrator.py -- Orquestrador principal do sistema multiagente
import os
import time
from datetime import datetime

from agents.analyst_agent import coletar_dados_analiticos, gerar_analise_executiva
from agents.ceo_agent import gerar_relatorio_ceo
from agents.sales_agent import gerar_relatorio_vendas

def exibir_cabecalho():
    print("\n" + "=" * 60)
    print("  Sistema Multiagente - Superstore Analytics")
    print("  Powered by Fábio Nogueira for Google Gemini + Agno Framework")
    print("=" * 60)
    print(f"  Execucao iniciada: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60 + "\n")

def exibir_progresso(etapa, total, descricao):
    print(f"\n[{etapa}/{total}] {descricao}")
    print("-" * 40)

def executar_pipeline():
    exibir_cabecalho()
    inicio = time.time()
    resultados = {}

    try:
        exibir_progresso(1, 4, "Agente Analista - Coletando dados")
        dados = coletar_dados_analiticos()
        resultados["dados"] = dados
        print(f"  OK Dados coletados: {len(dados)} dimensoes")

        exibir_progresso(2, 4, "Agente Analista - Gerando analise executiva")
        analise = gerar_analise_executiva(dados)
        resultados["analise"] = analise
        print(f"  OK Analise gerada: {len(analise.split())} palavras")

        exibir_progresso(3, 4, "Agente CEO - Gerando relatorio estrategico")
        relatorio_ceo = gerar_relatorio_ceo(analise, dados)
        resultados["relatorio_ceo"] = relatorio_ceo
        print(f"  OK Relatorio CEO: {len(relatorio_ceo.split())} palavras")

        exibir_progresso(4, 4, "Agente Vendas - Gerando relatorio operacional")
        relatorio_vendas = gerar_relatorio_vendas(analise, dados)
        resultados["relatorio_vendas"] = relatorio_vendas
        print(f"  OK Relatorio Vendas: {len(relatorio_vendas.split())} palavras")

    except Exception as e:
        print(f"\nERRO durante execucao: {e}")
        raise

    duracao = round(time.time() - inicio, 2)
    print("\n" + "=" * 60)
    print("  PIPELINE CONCLUIDO COM SUCESSO!")
    print("=" * 60)
    print(f"  Tempo total: {duracao}s")
    print(f"  Relatorios salvos em: reports/")
    print(f"  Arquivos gerados:")

    for arquivo in sorted(os.listdir("reports")):
        if arquivo.endswith(".md"):
            caminho = os.path.join("reports", arquivo)
            tamanho = os.path.getsize(caminho)
            print(f"      - {arquivo} ({tamanho:,} bytes)")

    print("=" * 60 + "\n")
    return resultados

if __name__ == "__main__":
    executar_pipeline()
