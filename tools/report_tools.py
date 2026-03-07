# tools/report_tools.py — Ferramentas de geração de relatórios em Markdown
import os
from datetime import datetime

# ── Configuração global ────────────────────────────────────────
PASTA_RELATORIOS = "reports"

def salvar_relatorio(nome_arquivo: str, conteudo: str) -> str:
    """
    Salva o relatório gerado em Markdown na pasta reports/.
    Retorna o caminho completo do arquivo salvo.
    """
    # Garante que a pasta existe
    os.makedirs(PASTA_RELATORIOS, exist_ok=True)

    # Adiciona timestamp no nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_final = f"{timestamp}_{nome_arquivo}.md"
    caminho = os.path.join(PASTA_RELATORIOS, nome_final)

    # Salva o arquivo
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

    print(f"📄 Relatório salvo em: {caminho}")
    return caminho