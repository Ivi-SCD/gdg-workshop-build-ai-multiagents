# Bloco 5 — Orquestrador e Sistema Multi-Agent Completo

Neste bloco final vamos unir todos os agentes com um **orquestrador** que delega tarefas automaticamente.

## 5.1 Como funciona o multi-agent no ADK?

No Google ADK, um agente pode ter **sub-agents**. O agente pai (orquestrador) decide automaticamente qual sub-agent chamar com base nas `description` de cada um.

```
         ┌─────────────────┐
         │  Orquestrador    │
         └────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐─────────────┐
    │             │             │             │
┌───▼───┐   ┌───▼────┐   ┌───▼────┐   ┌───▼────┐
│  RAG  │   │ Perfil │   │Mercado │   │Relatório│
└───────┘   └────────┘   └────────┘   └─────────┘
```

O fluxo é:
1. Usuário faz uma pergunta ao orquestrador
2. Orquestrador analisa a `description` de cada sub-agent
3. Delega para o agente mais adequado
4. Sub-agent responde usando suas tools
5. Orquestrador consolida e retorna ao usuário

## 5.2 Criando o orquestrador

```bash
mkdir -p agents/orchestrator
touch agents/orchestrator/__init__.py
touch agents/orchestrator/agent.py
```

```python
# agents/orchestrator/agent.py

from google.adk.agents import Agent

from agents.rag_agent.agent import rag_agent
from agents.profile_agent.agent import profile_agent
from agents.market_agent.agent import market_agent
from agents.report_agent.agent import report_agent

orchestrator = Agent(
    name="orchestrator",
    model="gemini-2.0-flash",
    description="Orquestrador do sistema de análise de investimentos.",
    instruction="""
    Você é o orquestrador de um sistema multi-agent de análise de investimentos.

    Você coordena os seguintes agentes especializados:

    1. **rag_agent**: Para perguntas conceituais sobre investimentos (o que é renda fixa, como funciona o tesouro direto, etc.)
    2. **profile_agent**: Para avaliar o perfil de investidor do usuário (conservador, moderado, arrojado)
    3. **market_agent**: Para consultar dados de mercado em tempo real (cotações de ações, câmbio, Selic)
    4. **report_agent**: Para gerar relatórios consolidados e exportar para Google Sheets

    Regras:
    - Delegue cada tarefa para o agente mais adequado
    - Você pode combinar informações de múltiplos agentes para dar uma resposta completa
    - Sempre seja claro sobre qual agente está utilizando
    - Se o usuário pedir uma análise completa, use múltiplos agentes em sequência
    - Inclua o disclaimer de que as informações são educacionais e não constituem recomendação de investimento

    Exemplo de fluxo completo:
    1. Usuário pede análise → você identifica o perfil (profile_agent)
    2. Busca dados de mercado relevantes (market_agent)
    3. Consulta conceitos necessários (rag_agent)
    4. Gera o relatório final (report_agent)
    """,
    sub_agents=[rag_agent, profile_agent, market_agent, report_agent],
)
```

```python
# agents/orchestrator/__init__.py

from .agent import orchestrator

root_agent = orchestrator
```

## 5.3 Atualizando o main.py

```python
# main.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.orchestrator import root_agent


async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="investment_advisor",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="investment_advisor",
        user_id="user",
    )

    print("=== Sistema Multi-Agent de Investimentos ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        user_input = input("Você: ").strip()

        if user_input.lower() in ("sair", "exit", "quit"):
            print("Até logo!")
            break

        if not user_input:
            continue

        message = Content(
            role="user",
            parts=[Part(text=user_input)],
        )

        response = runner.run(
            user_id="user",
            session_id=session.id,
            new_message=message,
        )

        print("\nAssistente: ", end="")
        async for event in response:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text)
        print()


if __name__ == "__main__":
    asyncio.run(main())
```

## 5.4 Testando o sistema completo

### Via interface web (recomendado para debug)

```bash
adk web agents/
```

Selecione **orchestrator** e teste:

1. "O que é tesouro direto?" → deve delegar para `rag_agent`
2. "Qual o preço da PETR4?" → deve delegar para `market_agent`
3. "Quero descobrir meu perfil de investidor" → deve delegar para `profile_agent`
4. "Gere um relatório completo" → deve usar vários agentes

### Via terminal

```bash
python main.py
```

### Fluxo completo de teste

```
Você: Quero fazer uma análise completa dos meus investimentos

→ Orquestrador identifica que precisa do perfil primeiro
→ Delega para profile_agent: faz perguntas sobre perfil

Você: Tenho tolerância média a risco, horizonte de 5 anos, pouca experiência, quero crescimento

→ profile_agent classifica como Moderado
→ Orquestrador busca dados de mercado via market_agent
→ Consulta base de conhecimento via rag_agent
→ Gera relatório via report_agent
→ Compartilha link do Google Sheets
```

## 5.5 Arquitetura final

```
gdg-workshop-build-ai-multiagents/
├── agents/
│   ├── __init__.py
│   ├── orchestrator/
│   │   ├── __init__.py
│   │   └── agent.py          # Agente orquestrador
│   ├── rag_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Agente de RAG
│   ├── profile_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Agente de perfil
│   ├── market_agent/
│   │   ├── __init__.py
│   │   └── agent.py          # Agente de mercado
│   └── report_agent/
│       ├── __init__.py
│       └── agent.py          # Agente de relatório
├── tools/
│   ├── __init__.py
│   ├── rag_tool.py            # Tool de busca na base de conhecimento
│   ├── market_tools.py        # Tools de dados de mercado (APIs)
│   └── sheets_tool.py         # Tool de exportação para Google Sheets
├── data/
│   ├── __init__.py
│   └── knowledge_base.py      # Base de conhecimento sobre investimentos
├── docs/
│   ├── BLOCO-1.md             # Google AI Studio
│   ├── BLOCO-2.md             # Primeiro agente com ADK
│   ├── BLOCO-3.md             # Agentes especializados
│   ├── BLOCO-4.md             # Agente de relatório + Sheets
│   └── BLOCO-5.md             # Orquestrador + sistema completo
├── main.py                     # Entrypoint CLI
├── requirements.txt
├── .env.example
├── .env                        # Suas keys (não commitar!)
├── .gitignore
├── CLAUDE.md
└── README.md
```

## 5.6 Recapitulação do Workshop

| Bloco | O que aprendemos |
|-------|------------------|
| 1 | Conceitos de IA generativa no Google AI Studio |
| 2 | Como criar um agente básico com Google ADK |
| 3 | Agentes especializados com tools (RAG, API, classificação) |
| 4 | Integração com Google Sheets para gerar artefatos |
| 5 | Orquestração multi-agent — o todo é maior que a soma das partes |

## 5.7 Próximos passos

- Melhorar o RAG com embeddings e busca vetorial
- Adicionar mais fontes de dados de mercado
- Implementar memória persistente entre sessões
- Deploy do sistema em Cloud Run ou Cloud Functions
- Adicionar autenticação de usuários

Parabéns! Você construiu um sistema multi-agent do zero.
