# Bloco 2 — Primeiro Agente com Google ADK

Neste bloco vamos criar nosso primeiro agente usando o **Google Agent Development Kit (ADK)**.

## 2.1 O que é o Google ADK?

O ADK é o framework do Google para construir agentes de IA. Ele oferece:

- Criação declarativa de agentes com instruções e tools
- Orquestração multi-agent nativa
- Integração direta com modelos Gemini
- Ferramentas prontas (Google Search, Code Execution, etc.)
- Interface web para debug (`adk web`)

## 2.2 Instalação

```bash
# Ative seu venv
source .venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

## 2.3 Estrutura de um agente no ADK

No ADK, cada agente é um **módulo Python** dentro de uma pasta com um `__init__.py` que exporta o agente como `root_agent`.

```
agents/
└── meu_agente/
    ├── __init__.py    # Exporta root_agent
    └── agent.py       # Define o agente
```

## 2.4 Criando o primeiro agente

Vamos criar um agente simples que responde perguntas sobre investimentos.

### Passo 1 — Criar a estrutura

```bash
mkdir -p agents/primeiro_agente
touch agents/__init__.py
touch agents/primeiro_agente/__init__.py
touch agents/primeiro_agente/agent.py
```

### Passo 2 — Definir o agente

```python
# agents/primeiro_agente/agent.py

from google.adk.agents import Agent

primeiro_agente = Agent(
    name="primeiro_agente",
    model="gemini-2.0-flash",
    description="Agente que responde perguntas básicas sobre investimentos.",
    instruction="""
    Você é um assistente especializado em investimentos.
    Responda de forma clara e didática.
    Sempre mencione que suas respostas são educacionais e não constituem recomendação de investimento.
    """,
)
```

### Passo 3 — Exportar como root_agent

```python
# agents/primeiro_agente/__init__.py

from .agent import primeiro_agente

root_agent = primeiro_agente
```

### Passo 4 — Testar com `adk web`

O ADK vem com uma interface web para testar agentes:

```bash
adk web agents/
```

Acesse `http://localhost:8000` no navegador, selecione `primeiro_agente` e converse com ele.

### Passo 5 — Testar via código

```python
# test_agent.py

import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.primeiro_agente import root_agent

async def main():
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="workshop",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="workshop",
        user_id="user",
    )

    message = Content(
        role="user",
        parts=[Part(text="O que é renda fixa?")],
    )

    response = runner.run(
        user_id="user",
        session_id=session.id,
        new_message=message,
    )

    async for event in response:
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text)

asyncio.run(main())
```

```bash
python test_agent.py
```

## 2.5 Adicionando uma Tool ao agente

Tools são funções Python que o agente pode chamar. Vamos criar uma tool simples:

```python
# agents/primeiro_agente/agent.py

from google.adk.agents import Agent

def calcular_rendimento(valor_inicial: float, taxa_anual: float, anos: int) -> dict:
    """Calcula o rendimento de um investimento com juros compostos.

    Args:
        valor_inicial: Valor investido inicialmente em reais.
        taxa_anual: Taxa de juros anual (ex: 0.12 para 12%).
        anos: Número de anos do investimento.

    Returns:
        dict com valor_final e rendimento_total.
    """
    valor_final = valor_inicial * (1 + taxa_anual) ** anos
    return {
        "valor_inicial": f"R$ {valor_inicial:,.2f}",
        "valor_final": f"R$ {valor_final:,.2f}",
        "rendimento_total": f"R$ {valor_final - valor_inicial:,.2f}",
        "anos": anos,
        "taxa_anual": f"{taxa_anual * 100:.1f}%",
    }

primeiro_agente = Agent(
    name="primeiro_agente",
    model="gemini-2.0-flash",
    description="Agente que responde perguntas básicas sobre investimentos.",
    instruction="""
    Você é um assistente especializado em investimentos.
    Responda de forma clara e didática.
    Sempre mencione que suas respostas são educacionais e não constituem recomendação de investimento.
    Use a ferramenta calcular_rendimento quando o usuário quiser simular investimentos.
    """,
    tools=[calcular_rendimento],
)
```

Teste novamente:

```bash
adk web agents/
```

Pergunte: "Quanto rende R$10.000 a 13% ao ano por 3 anos?"

O agente deve chamar a tool automaticamente e usar o resultado na resposta.

## 2.6 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| `Agent` | Unidade básica do ADK — tem nome, modelo, instruções e tools |
| `instruction` | System prompt do agente — define personalidade e comportamento |
| `tools` | Funções Python que o agente pode chamar quando necessário |
| `Runner` | Executa o agente e gerencia a conversação |
| `Session` | Mantém o histórico de uma conversa |
| `adk web` | Interface web para testar agentes visualmente |

Pronto para construir agentes especializados? Vamos para o [Bloco 3](BLOCO-3.md).
