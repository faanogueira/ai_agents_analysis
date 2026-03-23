# Superstore Analytics — Sistema Multiagente de IA

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange?logo=google&logoColor=white)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![IPOG](https://img.shields.io/badge/IPOG-Ciencia%20de%20Dados-purple)](https://www.ipog.edu.br/)
[![Status](https://img.shields.io/badge/Status-Concluido-brightgreen)]()

> **Projeto Integrador — Ciência de Dados | IPOG 2026**  
> Sistema multiagente baseado em IA que transforma dados brutos de varejo em relatórios executivos automatizados para CEO, Vendas e Logística.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Demonstração](#-demonstração)
- [Arquitetura](#-arquitetura)
- [Stack Tecnológica](#-stack-tecnológica)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Relatórios Gerados](#-relatórios-gerados)
- [Autor](#-autor)

---

## 📌 Sobre o Projeto

O **Superstore Analytics** é um sistema multiagente que utiliza Large Language Models (LLMs) para automatizar a análise de dados e geração de relatórios executivos personalizados.

O sistema analisa o dataset *Sample Superstore* (varejo USA 2014-2017) com **9.994 registros** e gera automaticamente 2 relatórios distintos, cada um adaptado ao perfil e necessidades do destinatário:

| Agente | Destinatário | Foco |
|---|---|---|
| 🔍 Analista | Interno | Coleta e interpreta os dados |
| 👔 CEO | C-Level | Decisões estratégicas e KPIs |
| 📈 Vendas | Time Comercial | Metas operacionais e ranking de produtos |

**Principais insights gerados automaticamente:**
- Margem de lucro por categoria, região e segmento
- Alertas críticos de subcategorias com prejuízo
- Impacto financeiro da política de descontos
- Tendência de crescimento YoY (2014-2017)
- Metas SMART para o próximo trimestre

---

## 🖥️ Demonstração

Rodando o pipeline (captura de tela)

[![Rodando o Pipeline](https://img.youtube.com/vi/6smQFyUhoD4/0.jpg)](https://www.youtube.com/watch?v=6smQFyUhoD4)


Saída do pipeline no terminal:

```
============================================================
  Sistema Multiagente - Superstore Analytics
  Powered by Fabio Nogueira + Google Gemini
============================================================
  Execucao iniciada: 06/03/2026 22:28:03
============================================================

[1/4] Agente Analista - Coletando dados
----------------------------------------
INFO  Agente Analista: coletando dados...
INFO  Agente Analista: dados coletados com sucesso!
  OK  Dados coletados: 7 dimensoes

[2/4] Agente Analista - Gerando analise executiva
----------------------------------------
INFO  Agente Analista: gerando analise executiva com Gemini...
INFO  Agente Analista: analise executiva gerada com sucesso!
  OK  Analise gerada: 1120 palavras

[3/4] Agente CEO - Gerando relatorio estrategico
----------------------------------------
INFO  Agente CEO: gerando relatorio estrategico...
INFO  Agente CEO: relatorio gerado com sucesso!
  OK  Relatorio CEO: 1310 palavras

[4/4] Agente Vendas - Gerando relatorio operacional
----------------------------------------
INFO  Agente Vendas: gerando relatorio operacional...
INFO  Agente Vendas: relatorio gerado com sucesso!
  OK  Relatorio Vendas: 1508 palavras

============================================================
  PIPELINE CONCLUIDO COM SUCESSO!
============================================================
  Tempo total: 89.15s
  Relatorios salvos em: reports/
============================================================
```

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                         │
│         Pipeline sequencial de 4 etapas                 │
└──────────────────────┬──────────────────────────────────┘
                       │
          ┌────────────▼────────────┐
          │     AGENTE ANALISTA     │
          │  Coleta dados via Tools │
          │  Interpreta com Gemini  │
          └────────────┬────────────┘
                       │ analise + dados
          ┌────────────▼────────────┐
          │                         │
  ┌───────▼───────┐       ┌─────────▼───────┐
  │  AGENTE CEO   │       │  AGENTE VENDAS  │
  │  Estrategico  │       │   Operacional   │
  └───────┬───────┘       └────────┬────────┘
          │                        │
          └───────────┬────────────┘
                      ▼
              reports/*.md
```

Para detalhes completos da arquitetura, padrões de projeto e decisões técnicas, consulte a [documentação técnica](docs/architecture.md).

---

## 🛠️ Stack Tecnológica

| Tecnologia | Uso |
|---|---|
| Python 3.12 | Linguagem principal |
| Google Gemini 2.5 Flash | Modelo de IA para geração de relatórios |
| google-genai 1.66.0 | Cliente oficial da API Gemini |
| pandas | Manipulação e análise do dataset |
| python-dotenv | Gerenciamento de variáveis de ambiente |
| Git | Versionamento do código |

---

## ✅ Pré-requisitos

- Python 3.10 ou superior
- Conta no [Google AI Studio](https://aistudio.google.com) para obter a API Key
- Dataset Superstore salvo em `data/` (instruções abaixo)
- Git instalado

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/faanogueira/ai_agents_analysis.git
cd ai_agents_analysis
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

> No Windows use: `venv\Scripts\activate`

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a API Key

Crie o arquivo `.env` na raiz do projeto:

```bash
echo "GEMINI_API_KEY=sua_chave_aqui" > .env
```

Obtenha sua chave gratuita em [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

### 5. Baixe o dataset

Acesse [kaggle.com/datasets/vivek468/superstore-dataset-final](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final), baixe o arquivo `Sample - Superstore.csv` e salve na pasta `data/`:

```bash
mkdir -p data
# Mova o arquivo baixado para:
# data/Sample - Superstore.csv
```

---

## 💻 Como Usar

### Executar o pipeline completo

```bash
python3 orchestrator.py
```

O sistema irá:
1. Validar o ambiente automaticamente
2. Coletar e processar os dados do dataset
3. Gerar análise executiva com IA
4. Salvar relatório estratégico (CEO) em `reports/`
5. Salvar relatório operacional (Vendas) em `reports/`

### Executar agentes individualmente

```bash
# Apenas o Agente Analista
python3 -m agents.analyst_agent

# Apenas o Agente CEO
python3 -m agents.ceo_agent

# Apenas o Agente Vendas
python3 -m agents.sales_agent
```

### Verificar logs de execução

```bash
cat logs/*.log
```

---

## 📁 Estrutura do Projeto

```
ai_agents_analysis/
├── agents/                      # Agentes de IA
│   ├── __init__.py
│   ├── analyst_agent.py         # Coleta e interpreta dados
│   ├── ceo_agent.py             # Relatorio estrategico CEO
│   └── sales_agent.py           # Relatorio operacional Vendas
├── data/                        # Dataset (nao versionado)
│   └── Sample - Superstore.csv
├── docs/                        # Documentacao tecnica
│   └── architecture.md          # Arquitetura do sistema
├── logs/                        # Logs de execucao
│   └── YYYYMMDD_pipeline.log
├── reports/                     # Relatorios gerados
│   └── YYYYMMDD_HHMMSS_*.md
├── tools/                       # Ferramentas Python
│   ├── __init__.py
│   ├── data_tools.py            # Consultas ao dataset
│   └── report_tools.py          # Geracao de arquivos
├── utils/                       # Utilitarios
│   ├── __init__.py
│   └── helpers.py               # Retry, logging, validacao
├── .env                         # API Key (nao versionado)
├── .gitignore
├── eda_superstore.py            # Analise exploratoria inicial
├── orchestrator.py              # Ponto de entrada principal
├── requirements.txt
└── README.md
```

---

## 📄 Relatórios Gerados

O sistema gera 2 relatórios em Markdown a cada execução, salvos em `reports/` com timestamp:

### Relatório CEO (`relatorio_ceo.md`)
Focado em decisões estratégicas de alto nível:
- Executive Summary com principais alertas
- KPIs estratégicos com status visual (Saudável / Atenção / Crítico)
- 3 decisões prioritárias com impacto financeiro estimado
- Top 3 riscos e oportunidades
- Plano de ação para os próximos 90 dias

### Relatório de Vendas (`relatorio_vendas.md`)
Focado em ações operacionais do time comercial:
- Performance regional detalhada com metas
- Análise por categoria e sub-categoria
- Perfil de clientes por segmento
- Impacto da política de descontos
- Metas SMART por região e categoria
- Ranking de produtos para impulsionar e revisar

---

## 👤 Autor

<!-- Início da seção "Contato" -->
<div>
  <p>Developed by <b>Fábio Nogueira</b></p>
</div>
<p>
<a href="https://www.linkedin.com/in/faanogueira/" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=13930&format=png&color=000000" target="_blank" width="80"></a>
<a href="https://github.com/faanogueira" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=AZOZNnY73haj&format=png&color=000000" target="_blank" width="80"></a>
<a href="https://api.whatsapp.com/send?phone=5571983937557" target="_blank"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=16713&format=png&color=000000" target="_blank" width="80"></a>
<a href="mailto:faanogueira@gmail.com"><img style="padding-right: 10px;" src="https://img.icons8.com/?size=100&id=P7UIlhbpWzZm&format=png&color=000000" target="_blank" width="80"></a> 
</p>
<!-- Fim da seção "Contato" -->

---

## 📜 Licença

Este projeto foi desenvolvido como Trabalho de Conclusão de Curso do programa de **Ciência de Dados** do **IPOG — Instituto de Pós-Graduação e Graduação**, sob orientação da Profa. Msc. Fabiana Rocha de Andrade e Silva.

Distribuído sob a licença MIT. Consulte o arquivo `LICENSE` para mais informações.
