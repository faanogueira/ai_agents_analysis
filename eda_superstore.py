# eda_superstore.py — Análise Exploratória do Dataset Superstore
import pandas as pd
import os

# ── Configurações ──────────────────────────────────────────────
CAMINHO_DADOS = "data/superstore.csv"

def carregar_dados():
    """Carrega o dataset com encoding correto."""
    df = pd.read_csv(CAMINHO_DADOS, encoding="latin-1")
    return df

def explorar_estrutura(df):
    """Exibe informações gerais do dataset."""
    print("=" * 50)
    print("📊 ESTRUTURA DO DATASET")
    print("=" * 50)
    print(f"Linhas:   {df.shape[0]:,}")
    print(f"Colunas:  {df.shape[1]}")
    print(f"\nColunas disponíveis:\n{list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos:\n{df.isnull().sum()}")

def explorar_negocios(df):
    """Exibe métricas de negócio relevantes."""
    print("\n" + "=" * 50)
    print("💰 VISÃO DE NEGÓCIO")
    print("=" * 50)

    # Converte datas
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    print(f"\nPeríodo: {df['Order Date'].min().date()} → {df['Order Date'].max().date()}")
    print(f"Total de pedidos:  {df['Order ID'].nunique():,}")
    print(f"Total de clientes: {df['Customer ID'].nunique():,}")
    print(f"Total de produtos: {df['Product ID'].nunique():,}")

    print(f"\n── Vendas por Categoria ──")
    print(df.groupby("Category")["Sales"].sum().round(2).sort_values(ascending=False))

    print(f"\n── Vendas por Região ──")
    print(df.groupby("Region")["Sales"].sum().round(2).sort_values(ascending=False))

    print(f"\n── Top 5 Sub-Categorias por Lucro ──")
    print(df.groupby("Sub-Category")["Profit"].sum().round(2).sort_values(ascending=False).head(5))

    print(f"\n── Bottom 5 Sub-Categorias por Lucro ──")
    print(df.groupby("Sub-Category")["Profit"].sum().round(2).sort_values().head(5))

if __name__ == "__main__":
    df = carregar_dados()
    explorar_estrutura(df)
    explorar_negocios(df)