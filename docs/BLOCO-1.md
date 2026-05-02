# Bloco 1 — Google ADK + Primeiro Agente

Neste bloco vamos configurar o ambiente, entender o Google ADK e construir nosso primeiro agente — um avaliador de perfil de investidor.

## 1.1 O que é o Google ADK?

O **Agent Development Kit (ADK)** é o framework do Google para construir agentes de IA. Ele oferece:

- Criação declarativa de agentes com instruções e tools
- Orquestração multi-agent nativa
- Integração direta com modelos Gemini
- Interface web para debug (`adk web`)

## 1.2 Setup do projeto

### Pré-requisitos

- Python 3.12+
- Conta Google

### Criando o ambiente

```bash
git clone https://github.com/Ivi-SCD/gdg-workshop-build-ai-multiagents.git
cd gdg-workshop-build-ai-multiagents

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt
```

### Criando sua API Key

1. Acesse [aistudio.google.com](https://aistudio.google.com/)
2. No menu lateral, clique em **"Get API Key"**
3. Clique em **"Create API Key"**
4. Selecione ou crie um projeto no Google Cloud
5. Copie a key gerada

```bash
cp .env.example .env
# Edite o .env e cole sua GOOGLE_API_KEY
```

### Testando a API Key

```python
# test_api.py

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explique o que é um agente de IA em uma frase."
)

print(response.text)
```

```bash
python test_api.py
```

Se obteve uma resposta, estamos prontos.

## 1.3 Estrutura de um agente no ADK

No ADK, cada agente é um **módulo Python** dentro de uma pasta com um `__init__.py` que exporta `root_agent`.

```
agents/
└── meu_agente/
    ├── __init__.py    # Exporta root_agent
    └── agent.py       # Define o agente
```

Conceitos fundamentais:

| Conceito | Descrição |
|----------|-----------|
| `Agent` | Unidade básica — tem nome, modelo, instruções e tools |
| `instruction` | System prompt — define personalidade e comportamento |
| `tools` | Funções Python que o agente pode chamar |
| `Runner` | Executa o agente e gerencia a conversação |
| `Session` | Mantém o histórico de uma conversa |
| `adk web` | Interface web para testar agentes visualmente |

## 1.4 Criando o primeiro agente: Perfil de Investidor

Nosso primeiro agente vai avaliar o perfil de risco do usuário (conservador, moderado, arrojado, agressivo) através de uma conversa e uma tool de classificação.

### Passo 1 — Criar a estrutura de pastas

```bash
mkdir -p agents/profile_agent
touch agents/__init__.py
touch agents/profile_agent/__init__.py
touch agents/profile_agent/agent.py
```

### Passo 2 — Definir a tool de classificação

A tool é uma função Python comum. O ADK usa o docstring e as type hints para gerar o schema que o modelo Gemini vai usar para chamar a função.

```python
# agents/profile_agent/agent.py

from google.adk.agents import Agent


def classify_profile(
    risk_tolerance: str,
    investment_horizon: str,
    experience: str,
    objective: str,
) -> dict:
    """Classifica o perfil do investidor com base nas respostas do usuário.

    Args:
        risk_tolerance: Tolerância a risco (baixa, media, alta).
        investment_horizon: Horizonte de investimento (curto, medio, longo).
        experience: Experiência com investimentos (nenhuma, pouca, moderada, muita).
        objective: Objetivo principal (preservar_capital, renda, crescimento, especulacao).

    Returns:
        dict com o perfil classificado e recomendações de alocação.
    """
    score = 0

    risk_scores = {"baixa": 1, "media": 2, "alta": 3}
    horizon_scores = {"curto": 1, "medio": 2, "longo": 3}
    experience_scores = {"nenhuma": 1, "pouca": 1, "moderada": 2, "muita": 3}
    objective_scores = {
        "preservar_capital": 1,
        "renda": 2,
        "crescimento": 3,
        "especulacao": 4,
    }

    score += risk_scores.get(risk_tolerance, 2)
    score += horizon_scores.get(investment_horizon, 2)
    score += experience_scores.get(experience, 1)
    score += objective_scores.get(objective, 2)

    if score <= 5:
        profile = "Conservador"
        allocation = "80% Renda Fixa, 15% Fundos Multimercado, 5% Renda Variável"
    elif score <= 8:
        profile = "Moderado"
        allocation = "50% Renda Fixa, 25% Fundos Multimercado, 25% Renda Variável"
    elif score <= 11:
        profile = "Arrojado"
        allocation = "25% Renda Fixa, 25% Fundos Multimercado, 50% Renda Variável"
    else:
        profile = "Agressivo"
        allocation = "10% Renda Fixa, 20% Fundos Multimercado, 70% Renda Variável"

    return {
        "perfil": profile,
        "score": score,
        "alocacao_recomendada": allocation,
        "tolerancia_risco": risk_tolerance,
        "horizonte": investment_horizon,
    }
```

### Passo 3 — Definir o agente

Adicione o agente no mesmo arquivo, logo após a tool:

```python
# agents/profile_agent/agent.py (continuação)

profile_agent = Agent(
    name="profile_agent",
    model="gemini-2.0-flash",
    description="Agente que avalia o perfil de investidor do usuário através de perguntas.",
    instruction="""
    Você é um agente especializado em avaliação de perfil de investidor.

    Seu trabalho é fazer perguntas ao usuário para entender:
    1. Tolerância a risco (baixa, media, alta)
    2. Horizonte de investimento (curto: até 1 ano, medio: 1-5 anos, longo: 5+ anos)
    3. Experiência com investimentos (nenhuma, pouca, moderada, muita)
    4. Objetivo principal (preservar_capital, renda, crescimento, especulacao)

    Faça as perguntas de forma conversacional e amigável, uma de cada vez.
    Quando tiver todas as respostas, use a ferramenta classify_profile para classificar.
    Apresente o resultado de forma clara e explique o que cada perfil significa.
    Sempre mencione que a análise é educacional e não constitui recomendação de investimento.
    """,
    tools=[classify_profile],
)
```

### Passo 4 — Exportar como root_agent

```python
# agents/profile_agent/__init__.py

from .agent import profile_agent

root_agent = profile_agent
```

### Passo 5 — Testar com `adk web`

O ADK vem com uma interface web para testar agentes:

```bash
adk web agents/
```

Acesse `http://localhost:8000` no navegador, selecione **profile_agent** e converse:

```
Você: Quero descobrir meu perfil de investidor
Agente: Ótimo! Vou te fazer algumas perguntas...
```

O agente deve fazer as perguntas, chamar a tool `classify_profile` automaticamente e apresentar o resultado.

### Passo 6 — Testar via código

```python
# test_agent.py

import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "agents"))

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from profile_agent import root_agent


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
        parts=[Part(text="Quero descobrir meu perfil de investidor")],
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

## 1.5 Conceitos-chave aprendidos

- **Google ADK**: framework para criar agentes com Gemini
- **Agent**: unidade básica com instrução + tools
- **Tools**: funções Python que o modelo decide quando chamar (function calling)
- **`adk web`**: interface para testar agentes visualmente
- **Perfil de investidor**: nosso primeiro agente funcional

Pronto para construir o agente de RAG? Vamos para o [Bloco 2](BLOCO-2.md).
