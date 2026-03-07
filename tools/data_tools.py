# tools/data_tools.py — Ferramentas de consulta e análise do dataset Superstore
import pandas as pd

# ── Configuração global ────────────────────────────────────────
CAMINHO_DADOS = "data/superstore.csv"

def _carregar_dados() -> pd.DataFrame:
    """Carrega o dataset. Função interna usada pelas tools."""
    df = pd.read_csv(CAMINHO_DADOS, encoding="latin-1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    return df

# ── Tools de Visão Geral ───────────────────────────────────────

def obter_resumo_geral() -> dict:
    """
    Retorna métricas gerais do negócio.
    Usada pelo Agente CEO para visão macro.
    """
    df = _carregar_dados()
    return {
        "periodo_inicio": str(df["Order Date"].min().date()),
        "periodo_fim": str(df["Order Date"].max().date()),
        "total_vendas": round(df["Sales"].sum(), 2),
        "total_lucro": round(df["Profit"].sum(), 2),
        "margem_lucro_pct": round((df["Profit"].sum() / df["Sales"].sum()) * 100, 2),
        "total_pedidos": df["Order ID"].nunique(),
        "total_clientes": df["Customer ID"].nunique(),
        "total_produtos": df["Product ID"].nunique(),
    }

def vendas_por_categoria() -> dict:
    """
    Retorna vendas, lucro e margem por categoria.
    Usada pelo Agente CEO e Agente de Vendas.
    """
    df = _carregar_dados()
    grupo = df.groupby("Category").agg(
        vendas=("Sales", "sum"),
        lucro=("Profit", "sum"),
        pedidos=("Order ID", "nunique")
    ).round(2)
    grupo["margem_pct"] = (grupo["lucro"] / grupo["vendas"] * 100).round(2)
    return grupo.sort_values("vendas", ascending=False).to_dict(orient="index")

def vendas_por_regiao() -> dict:
    """
    Retorna vendas, lucro e margem por região.
    Usada pelo Agente de Vendas para análise regional.
    """
    df = _carregar_dados()
    grupo = df.groupby("Region").agg(
        vendas=("Sales", "sum"),
        lucro=("Profit", "sum"),
        pedidos=("Order ID", "nunique")
    ).round(2)
    grupo["margem_pct"] = (grupo["lucro"] / grupo["vendas"] * 100).round(2)
    return grupo.sort_values("vendas", ascending=False).to_dict(orient="index")

def top_subcategorias_lucro(top_n: int = 5) -> dict:
    """
    Retorna as sub-categorias mais e menos lucrativas.
    Usada pelo Agente CEO para alertas estratégicos.
    """
    df = _carregar_dados()
    grupo = df.groupby("Sub-Category").agg(
        vendas=("Sales", "sum"),
        lucro=("Profit", "sum")
    ).round(2)
    grupo["margem_pct"] = (grupo["lucro"] / grupo["vendas"] * 100).round(2)
    grupo = grupo.sort_values("lucro", ascending=False)
    return {
        "top_lucrativas": grupo.head(top_n).to_dict(orient="index"),
        "bottom_lucrativas": grupo.tail(top_n).to_dict(orient="index"),
    }

def tendencia_vendas_anual() -> dict:
    """
    Retorna evolução de vendas e lucro por ano.
    Usada pelo Agente CEO para análise de crescimento YoY.
    """
    df = _carregar_dados()
    df["ano"] = df["Order Date"].dt.year
    grupo = df.groupby("ano").agg(
        vendas=("Sales", "sum"),
        lucro=("Profit", "sum"),
        pedidos=("Order ID", "nunique")
    ).round(2)
    grupo["margem_pct"] = (grupo["lucro"] / grupo["vendas"] * 100).round(2)
    return grupo.to_dict(orient="index")

def vendas_por_segmento() -> dict:
    """
    Retorna vendas e lucro por segmento de cliente.
    Usada pelo Agente de Vendas para análise de perfil.
    """
    df = _carregar_dados()
    grupo = df.groupby("Segment").agg(
        vendas=("Sales", "sum"),
        lucro=("Profit", "sum"),
        clientes=("Customer ID", "nunique")
    ).round(2)
    grupo["margem_pct"] = (grupo["lucro"] / grupo["vendas"] * 100).round(2)
    return grupo.sort_values("vendas", ascending=False).to_dict(orient="index")

def impacto_desconto() -> dict:
    """
    Analisa correlação entre desconto e lucro por categoria.
    Usada pelo Agente CEO para alertas de política comercial.
    """
    df = _carregar_dados()
    # Agrupa por faixa de desconto
    df["faixa_desconto"] = pd.cut(
        df["Discount"],
        bins=[-0.01, 0, 0.2, 0.4, 1.0],
        labels=["Sem desconto", "Até 20%", "20-40%", "Acima 40%"]
    )
    grupo = df.groupby("faixa_desconto", observed=True).agg(
        total_pedidos=("Order ID", "count"),
        lucro_medio=("Profit", "mean"),
        vendas_total=("Sales", "sum")
    ).round(2)
    return grupo.to_dict(orient="index")