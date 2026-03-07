# Arquitetura do Sistema Multiagente — Superstore Analytics

**Autor:** Fábio Nogueira  
**Instituição:** IPOG — Instituto de Pós-Graduação e Graduação  
**Curso:** Ciência de Dados  
**Disciplina:** Projeto Integrador — Semestre Final  
**Data:** Março/2026  

---

## Visão Geral

O **Superstore Analytics** é um sistema multiagente baseado em IA que analisa
automaticamente dados de vendas do varejo e gera relatórios executivos
personalizados para diferentes níveis hierárquicos da organização.

O sistema transforma dados brutos do dataset *Sample Superstore* (varejo USA
2014-2017) em insights acionáveis para CEO, Gerência de Vendas e Logística,
sem intervenção humana no processo analítico.

---

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                         │
│              (orchestrator.py)                          │
│         Pipeline sequencial de 4 etapas                 │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │     AGENTE ANALISTA     │
          │   analyst_agent.py      │
          │                         │
          │  1. Coleta dados via    │
          │     Tools Python        │
          │  2. Envia ao Gemini     │
          │  3. Retorna analise     │
          │     estruturada         │
          └────────────┬────────────┘
                       │ analise_executiva + dados
          ┌────────────▼────────────┐
          │                         │
  ┌───────▼───────┐       ┌─────────▼───────┐
  │  AGENTE CEO   │       │  AGENTE VENDAS  │
  │ ceo_agent.py  │       │sales_agent.py   │
  │               │       │                 │
  │  Relatorio    │       │  Relatorio      │
  │  Estrategico  │       │  Operacional    │
  │  (CEO)        │       │  (Comercial)    │
  └───────┬───────┘       └────────┬────────┘
          │                        │
          └───────────┬────────────┘
                      │
          ┌───────────▼────────────┐
          │    reports/*.md        │
          │  Arquivos Markdown     │
          │  com timestamp         │
          └────────────────────────┘
```

---

## Componentes do Sistema

### 1. Orquestrador (`orchestrator.py`)

Responsável por coordenar a execução sequencial de todos os agentes.

**Responsabilidades:**
- Validar o ambiente antes da execução (API Key, dataset, pastas)
- Executar o pipeline em ordem definida
- Exibir progresso em tempo real no terminal
- Consolidar o resumo final com arquivos gerados e tempo de execução

**Fluxo de execução:**
```
validar_ambiente()
    → coletar_dados_analiticos()
    → gerar_analise_executiva()
    → gerar_relatorio_ceo()
    → gerar_relatorio_vendas()
```

---

### 2. Agente Analista (`agents/analyst_agent.py`)

Primeiro agente do pipeline. Responsável por coletar, processar e
interpretar os dados brutos do dataset.

**Responsabilidades:**
- Invocar todas as tools de análise de dados
- Serializar os dados em JSON estruturado
- Enviar os dados ao Gemini com prompt especializado
- Retornar análise executiva em Markdown

**Prompt Strategy:** O agente usa um prompt de *role-playing* onde o
modelo assume o papel de "analista sênior de dados com experiência em
varejo", garantindo linguagem e profundidade adequadas.

---

### 3. Agente CEO (`agents/ceo_agent.py`)

Segundo agente do pipeline. Consome a análise do Agente Analista e
gera um relatório estratégico para o nível C-Level.

**Responsabilidades:**
- Receber análise executiva e dados brutos
- Gerar relatório com KPIs, decisões estratégicas e plano de 90 dias
- Salvar relatório em Markdown com timestamp

**Estrutura do Relatório:**
- Executive Summary
- KPIs Estratégicos (com status visual)
- Decisões Estratégicas Recomendadas
- Riscos Identificados
- Oportunidades de Crescimento
- Próximos Passos — 90 dias

---

### 4. Agente Vendas (`agents/sales_agent.py`)

Terceiro agente do pipeline. Gera relatório operacional focado no
time comercial e gerência de vendas.

**Responsabilidades:**
- Receber análise executiva e dados brutos
- Gerar relatório com metas SMART e ranking de produtos
- Salvar relatório em Markdown com timestamp

**Estrutura do Relatório:**
- Resumo de Performance
- Performance Regional Detalhada
- Análise por Categoria e Sub-Categoria
- Perfil dos Clientes por Segmento
- Impacto de Descontos
- Metas e Ações para o Próximo Trimestre
- Ranking de Produtos — Foco Imediato

---

### 5. Tools de Dados (`tools/data_tools.py`)

Conjunto de funções Python que encapsulam toda a lógica de consulta
e transformação do dataset. São as "mãos" do Agente Analista.

| Função | Descrição |
|---|---|
| `obter_resumo_geral()` | KPIs macro: vendas, lucro, margem, clientes |
| `vendas_por_categoria()` | Vendas, lucro e margem por categoria |
| `vendas_por_regiao()` | Performance por região geográfica |
| `top_subcategorias_lucro()` | Ranking de sub-categorias por lucro |
| `tendencia_vendas_anual()` | Evolução YoY de vendas e lucro |
| `vendas_por_segmento()` | Análise por segmento de cliente |
| `impacto_desconto()` | Correlação entre desconto e lucro |

---

### 6. Tools de Relatório (`tools/report_tools.py`)

Responsável por persistir os relatórios gerados em arquivos Markdown.

**Funcionalidades:**
- Criação automática da pasta `reports/` se não existir
- Nomenclatura com timestamp (`YYYYMMDD_HHMMSS_nome.md`)
- Encoding UTF-8 para suporte a caracteres especiais

---

### 7. Utilitários (`utils/helpers.py`)

Módulo de resiliência e observabilidade do sistema.

**Funcionalidades:**

**Retry Automático (`com_retry`):**
- Até 3 tentativas em caso de falha
- Tratamento específico para erro 429 (quota da API)
- Espera configurável entre tentativas (padrão: 60s)
- Tratamento diferenciado para erros de autenticação

**Validação de Ambiente (`validar_ambiente`):**
- Verifica presença da `GEMINI_API_KEY` no `.env`
- Verifica existência do dataset
- Cria pastas necessárias automaticamente

**Logging Estruturado:**
- Logs simultâneos em arquivo (`logs/YYYYMMDD_pipeline.log`) e terminal
- Níveis: INFO, WARNING, ERROR
- Formato: `timestamp [LEVEL] mensagem`

---

## Stack Tecnológica

| Componente | Tecnologia | Versão |
|---|---|---|
| Linguagem | Python | 3.12 |
| Modelo de IA | Google Gemini 2.5 Flash | via API |
| Cliente API | google-genai | 1.66.0 |
| Manipulação de dados | pandas | latest |
| Variáveis de ambiente | python-dotenv | latest |
| Versionamento | Git | latest |

---

## Dataset

**Nome:** Sample Superstore  
**Fonte:** Kaggle (vivek468/superstore-dataset-final)  
**Período:** Janeiro/2014 — Dezembro/2017  
**Volume:** 9.994 registros, 21 colunas  
**Qualidade:** Sem valores nulos  

**Colunas principais:**

| Coluna | Tipo | Descrição |
|---|---|---|
| Order ID | string | Identificador único do pedido |
| Order Date | date | Data do pedido |
| Ship Mode | string | Modalidade de envio |
| Customer ID | string | Identificador do cliente |
| Segment | string | Segmento (Consumer/Corporate/Home Office) |
| Region | string | Região geográfica (West/East/Central/South) |
| Category | string | Categoria do produto |
| Sub-Category | string | Sub-categoria do produto |
| Sales | float | Valor de venda |
| Quantity | int | Quantidade vendida |
| Discount | float | Percentual de desconto |
| Profit | float | Lucro do pedido |

---

## Padrões de Projeto Aplicados

**1. Pipeline Pattern**  
O sistema executa etapas sequenciais onde a saída de uma etapa é
a entrada da próxima, garantindo rastreabilidade e modularidade.

**2. Separation of Concerns**  
Cada módulo tem responsabilidade única e bem definida:
tools coletam dados, agents processam com IA, utils garantem resiliência.

**3. Retry Pattern**  
Resiliência a falhas transitórias da API através de re-tentativas
com backoff configurável.

**4. Structured Logging**  
Observabilidade completa do pipeline com logs persistidos em arquivo
para auditoria e debugging.

---

## Estrutura de Pastas

```
ai_agents_analysis/
├── agents/                  # Agentes de IA
│   ├── __init__.py
│   ├── analyst_agent.py     # Agente Analista
│   ├── ceo_agent.py         # Agente CEO
│   └── sales_agent.py       # Agente Vendas
├── data/                    # Dataset
│   └── Sample - Superstore.csv
├── docs/                    # Documentação técnica
│   └── architecture.md      # Este arquivo
├── logs/                    # Logs de execução
│   └── YYYYMMDD_pipeline.log
├── reports/                 # Relatórios gerados
│   └── YYYYMMDD_HHMMSS_relatorio_*.md
├── tools/                   # Ferramentas Python
│   ├── __init__.py
│   ├── data_tools.py        # Consultas ao dataset
│   └── report_tools.py      # Geração de arquivos
├── utils/                   # Utilitários
│   ├── __init__.py
│   └── helpers.py           # Retry, logging, validação
├── venv/                    # Ambiente virtual Python
├── .env                     # Chave API (não versionado)
├── .gitignore
├── eda_superstore.py        # Análise exploratória inicial
├── orchestrator.py          # Ponto de entrada principal
├── requirements.txt
└── README.md
```

---

## Como Executar

### Pré-requisitos
```bash
# Python 3.12+
python3 --version

# Clonar o repositório
git clone <url-do-repositorio>
cd ai_agents_analysis

# Criar e ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Configuração
```bash
# Criar arquivo .env com a chave da API
echo "GEMINI_API_KEY=sua_chave_aqui" > .env

# Baixar o dataset e salvar em data/
# https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
```

### Execução
```bash
# Rodar o pipeline completo
python3 orchestrator.py

# Rodar agentes individualmente
python3 -m agents.analyst_agent
python3 -m agents.ceo_agent
python3 -m agents.sales_agent
```

### Output esperado
```
Sistema Multiagente - Superstore Analytics
[1/4] Agente Analista - Coletando dados         ✅
[2/4] Agente Analista - Gerando analise          ✅
[3/4] Agente CEO - Gerando relatorio             ✅
[4/4] Agente Vendas - Gerando relatorio          ✅
PIPELINE CONCLUIDO COM SUCESSO!
Tempo total: ~90s
```

---

## Decisões Técnicas

**Por que Google Gemini e não OpenAI?**  
O Gemini 2.5 Flash oferece tier gratuito generoso para desenvolvimento,
suporte nativo via `google-genai` e qualidade de geração de texto
equivalente para casos de uso de relatórios estruturados.

**Por que pipeline sequencial e não paralelo?**  
Os agentes CEO e Vendas dependem da análise do Agente Analista.
A execução paralela exigiria sincronização adicional sem ganho
significativo de performance para o escopo do projeto.

**Por que Markdown como formato de saída?**  
Markdown é legível por humanos, renderizável em qualquer plataforma
(GitHub, Notion, VS Code) e facilmente convertível para PDF ou HTML
para apresentações executivas.
