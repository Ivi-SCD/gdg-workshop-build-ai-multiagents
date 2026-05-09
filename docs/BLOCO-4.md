# Bloco 4 — Sistema Multi-Agent Completo

Neste bloco final vamos unir todos os agentes com um **orquestrador** que delega tarefas automaticamente, construindo o sistema multi-agent completo.

## 4.1 Arquitetura Multi-Agent no ADK

No Google ADK, um agente pode ter **sub_agents**. O agente pai (orquestrador) decide automaticamente qual sub-agent chamar com base na `description` de cada um.

```
                    ┌────────────────────┐
                    │   Orquestrador     │
                    │   (coordena tudo)  │
                    └─────────┬──────────┘
                              │
          ┌───────────┬───────┴───────┬────────────┐
          │           │               │            │
    ┌─────▼─────┐ ┌──▼──────┐ ┌─────▼──────┐ ┌───▼────────┐
    │  Perfil   │ │   RAG   │ │  Mercado   │ │ Relatório  │
    │ Investidor│ │         │ │            │ │ + Sheets   │
    └───────────┘ └─────────┘ └────────────┘ └────────────┘
     classify_     search_      get_stock_     export_report_
     profile()     knowledge_   quote()        to_sheets()
                   base()       get_stock_     list_reports()
                                history()
                                get_currency_
                                rate()
                                get_selic_
                                rate()
```

O fluxo:
1. Usuário faz uma pergunta ao orquestrador
2. Orquestrador analisa a `description` de cada sub-agent
3. Delega para o agente mais adequado
4. Sub-agent responde usando suas tools
5. Orquestrador pode chamar múltiplos agentes em sequência
6. Retorna a resposta consolidada ao usuário

## 4.2 Criando o orquestrador

```bash
mkdir -p agents/orchestrator
```

```python
# agents/orchestrator/agent.py

from google.adk.agents import Agent

from profile_agent.agent import profile_agent
from rag_agent.agent import rag_agent
from market_agent.agent import market_agent
from report_agent.agent import report_agent

orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.5-flash",
    description="Orquestrador do sistema de análise de investimentos.",
    instruction="""
    Você é o orquestrador de um sistema multi-agent de análise de investimentos.

    Você coordena os seguintes agentes especializados:

    1. **profile_agent**: Para avaliar o perfil de investidor do usuário (conservador, moderado, arrojado, agressivo). Use quando o usuário quer descobrir seu perfil ou quando precisa de uma recomendação personalizada.

    2. **rag_agent**: Para perguntas conceituais sobre investimentos (o que é renda fixa, como funciona tesouro direto, o que são ETFs, etc.). Use quando o usuário quer aprender ou entender conceitos.

    3. **market_agent**: Para consultar dados de mercado em tempo real (cotações de ações, câmbio, Selic). Use quando o usuário quer saber preços, cotações ou dados atuais do mercado.

    4. **report_agent**: Para gerar relatórios consolidados e exportar para Google Sheets. Use quando o usuário quer um relatório formal ou exportar dados.

    REGRAS:
    - Delegue cada tarefa para o agente mais adequado
    - Para análises completas, use múltiplos agentes em sequência:
      1. Primeiro descubra o perfil (profile_agent)
      2. Busque dados de mercado relevantes (market_agent)
      3. Consulte conceitos se necessário (rag_agent)
      4. Gere o relatório final (report_agent)
    - Seja claro sobre o que está fazendo em cada etapa
    - Inclua o disclaimer de que as informações são educacionais
    """,
    sub_agents=[profile_agent, rag_agent, market_agent, report_agent],
)
```

```python
# agents/orchestrator/__init__.py

from .agent import orchestrator

root_agent = orchestrator
```

## 4.3 Testando o sistema completo

### Via interface web (recomendado para debug)

```bash
adk web agents/
```

Selecione **orchestrator** e teste cada cenário:

### Teste 1 — Delegação para perfil

```
Você: Quero descobrir meu perfil de investidor
→ Orquestrador delega para profile_agent
→ profile_agent faz perguntas e classifica
```

### Teste 2 — Delegação para RAG

```
Você: O que é tesouro direto?
→ Orquestrador delega para rag_agent
→ rag_agent busca na base e explica
```

### Teste 3 — Delegação para mercado

```
Você: Qual o preço da PETR4 e do dólar hoje?
→ Orquestrador delega para market_agent
→ market_agent chama get_stock_quote e get_currency_rate
```

### Teste 4 — Fluxo completo (múltiplos agentes)

```
Você: Quero uma análise completa dos meus investimentos.
      Sou conservador, invisto a longo prazo, tenho pouca experiência
      e meu objetivo é crescimento.

→ Orquestrador:
  1. Delega para profile_agent → classifica perfil
  2. Delega para market_agent → busca cotações relevantes
  3. Delega para rag_agent → busca conceitos sobre o perfil
  4. Delega para report_agent → gera relatório no Google Sheets
  5. Retorna resposta consolidada com link da planilha
```


## 4.4 Arquitetura final do projeto

```
gdg-workshop-build-ai-multiagents/
├── agents/
│   ├── __init__.py
│   ├── orchestrator/          # Bloco 4
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── profile_agent/         # Bloco 1
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── rag_agent/             # Bloco 2
│   │   ├── __init__.py
│   │   └── agent.py
│   ├── market_agent/          # Bloco 3
│   │   ├── __init__.py
│   │   └── agent.py
│   └── report_agent/          # Bloco 3
│       ├── __init__.py
│       └── agent.py
│   ├── rag_agent/             # Bloco 2
│   │   ├── tools/rag_tools.py
│   │   └── data/knowledge_base.py
│   ├── market_agent/          # Bloco 3
│   │   └── tools/market_tools.py
│   └── report_agent/          # Bloco 3
│       └── tools/sheets_tool.py
├── docs/
│   ├── BLOCO-1.md             # Google ADK + Agente de Perfil
│   ├── BLOCO-2.md             # Agente RAG
│   ├── BLOCO-3.md             # Agente Mercado + Relatório
│   └── BLOCO-4.md             # Sistema Multi-Agent
├── requirements.txt
├── .env.example
├── .env
├── credentials.json           # NÃO commitar!
├── .gitignore
├── CLAUDE.md
└── README.md
```

## 4.6 Recapitulação do Workshop

| Bloco | O que construímos |
|-------|-------------------|
| 1 | Setup + Google ADK + Agente de Perfil de Investidor (com tool de classificação) |
| 2 | Agente RAG com base de conhecimento sobre investimentos |
| 3 | Agente de Mercado (yfinance, câmbio, Selic) + Agente de Relatório (Google Sheets) |
| 4 | Orquestrador multi-agent que coordena todos os agentes |

## 4.7 O que aprendemos

- **Google ADK** como framework para agentes de IA
- **Function Calling** — o modelo decide quando e como usar ferramentas
- **RAG** — fundamentar respostas em dados reais
- **APIs públicas** — integrar dados de mercado em tempo real
- **Google Sheets API** — gerar artefatos externos
- **Multi-agent** — orquestração onde o todo é maior que a soma das partes

## 4.8 Próximos passos

- Melhorar o RAG com embeddings e busca vetorial (Vertex AI, ChromaDB)
- Adicionar mais fontes de dados (fundos, FIIs, criptomoedas)
- Implementar memória persistente entre sessões
- Deploy em Cloud Run ou Cloud Functions
- Adicionar autenticação de usuários
- Usar Gemini 2.5 com thinking para análises mais complexas

Parabéns! Você construiu um sistema multi-agent do zero usando Google ADK.
