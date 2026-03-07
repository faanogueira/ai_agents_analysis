# test_tools.py — Valida se todas as tools estão funcionando
from tools.data_tools import (
    obter_resumo_geral,
    vendas_por_categoria,
    vendas_por_regiao,
    top_subcategorias_lucro,
    tendencia_vendas_anual,
    vendas_por_segmento,
    impacto_desconto,
)

print("🔧 Testando tools do Agente Analista...\n")

print("── Resumo Geral ──")
print(obter_resumo_geral())

print("\n── Vendas por Categoria ──")
print(vendas_por_categoria())

print("\n── Vendas por Região ──")
print(vendas_por_regiao())

print("\n── Top Sub-categorias ──")
print(top_subcategorias_lucro())

print("\n── Tendência Anual ──")
print(tendencia_vendas_anual())

print("\n── Vendas por Segmento ──")
print(vendas_por_segmento())

print("\n── Impacto do Desconto ──")
print(impacto_desconto())

print("\n✅ Todas as tools funcionando!")