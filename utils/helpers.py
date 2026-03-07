# utils/helpers.py -- Utilitarios de resiliencia, validacao e logging
import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Configuracao de Logging ────────────────────────────────────
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # Salva logs em arquivo com data
        logging.FileHandler(
            f"logs/{datetime.now().strftime('%Y%m%d')}_pipeline.log",
            encoding="utf-8"
        ),
        # Exibe logs no terminal tambem
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ── Validacao de Ambiente ──────────────────────────────────────

def validar_ambiente() -> bool:
    """
    Valida se todos os requisitos estao presentes antes de rodar.
    Retorna True se OK, levanta excecao se algum requisito faltar.
    """
    erros = []

    # Verifica API Key
    if not os.getenv("GEMINI_API_KEY"):
        erros.append("GEMINI_API_KEY nao encontrada no arquivo .env")

    # Verifica dataset
    dataset = "data/Sample - Superstore.csv"
    if not os.path.exists(dataset):
        erros.append(f"Dataset nao encontrado: {dataset}")

    # Verifica pastas necessarias
    for pasta in ["agents", "tools", "reports", "logs"]:
        if not os.path.exists(pasta):
            os.makedirs(pasta, exist_ok=True)
            logger.info(f"Pasta criada: {pasta}")

    if erros:
        for erro in erros:
            logger.error(f"ERRO DE AMBIENTE: {erro}")
        raise EnvironmentError(
            f"Ambiente invalido. Corrija os erros:\n" + "\n".join(erros)
        )

    logger.info("Ambiente validado com sucesso!")
    return True


# ── Retry Automatico ───────────────────────────────────────────

def com_retry(funcao, max_tentativas: int = 3, espera_segundos: int = 60):
    """
    Executa uma funcao com retry automatico em caso de falha.
    Util para lidar com erros de quota da API do Gemini (erro 429).

    Uso:
        resultado = com_retry(lambda: cliente.models.generate_content(...))
    """
    for tentativa in range(1, max_tentativas + 1):
        try:
            return funcao()

        except Exception as e:
            erro_str = str(e)

            # Erro de quota -- aguarda e tenta novamente
            if "429" in erro_str or "RESOURCE_EXHAUSTED" in erro_str:
                if tentativa < max_tentativas:
                    logger.warning(
                        f"Quota da API atingida. "
                        f"Tentativa {tentativa}/{max_tentativas}. "
                        f"Aguardando {espera_segundos}s..."
                    )
                    time.sleep(espera_segundos)
                    continue
                else:
                    logger.error("Quota da API esgotada apos todas as tentativas.")
                    raise

            # Erro de autenticacao -- nao tenta novamente
            elif "401" in erro_str or "API_KEY" in erro_str:
                logger.error("Erro de autenticacao. Verifique sua GEMINI_API_KEY.")
                raise

            # Outros erros -- tenta novamente com espera menor
            else:
                if tentativa < max_tentativas:
                    logger.warning(
                        f"Erro inesperado: {erro_str[:100]}. "
                        f"Tentativa {tentativa}/{max_tentativas}. "
                        f"Aguardando 10s..."
                    )
                    time.sleep(10)
                    continue
                else:
                    logger.error(f"Falha apos {max_tentativas} tentativas: {erro_str}")
                    raise