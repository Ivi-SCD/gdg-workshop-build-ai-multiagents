# Do 0 ao Multi-Agent com Google ADK

Workshop prático onde você vai sair do zero até construir um sistema multi-agent completo para análise de investimentos usando o **Google Agent Development Kit (ADK)**.

## Palestrantes

| Nome | Contato |
|------|---------|
| **Ivisson Alves** | <!-- adicionar links --> |
| **Giulia Buonafina** | <!-- adicionar links --> |

## O que vamos construir?

Um sistema multi-agent de análise de investimentos composto por:

- **Agente Orquestrador** — recebe perguntas e delega para agentes especializados
- **Agente de RAG** — busca em base de conhecimento sobre investimentos
- **Agente de Perfil de Investidor** — avalia o perfil de risco do usuário
- **Agente de Mercado** — consulta APIs públicas para dados em tempo real
- **Agente de Relatório** — gera relatório consolidado e exporta para Google Sheets

## Pré-requisitos

- Python 3.12+
- Conta Google (para Google AI Studio e API Key)
- Git

## Setup rápido

```bash
git clone https://github.com/seu-usuario/gdg-workshop-build-ai-multiagents.git
cd gdg-workshop-build-ai-multiagents

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt

cp .env.example .env
# Edite o .env com sua API Key
```

## Roteiro do Workshop

| Bloco | Tema | Doc |
|-------|------|-----|
| 1 | Google AI Studio — conceitos e playground | [BLOCO-1](docs/BLOCO-1.md) |
| 2 | Primeiro agente com Google ADK | [BLOCO-2](docs/BLOCO-2.md) |
| 3 | Agentes especializados (RAG, Perfil, Mercado) | [BLOCO-3](docs/BLOCO-3.md) |
| 4 | Agente de Relatório + Google Sheets | [BLOCO-4](docs/BLOCO-4.md) |
| 5 | Orquestrador e sistema multi-agent completo | [BLOCO-5](docs/BLOCO-5.md) |

## Estrutura do projeto

```
├── agents/            # Código dos agentes
├── tools/             # Ferramentas (tools) dos agentes
├── data/              # Dados para RAG
├── docs/              # Guias passo a passo (BLOCO-*.md)
├── main.py            # Entrypoint do sistema multi-agent
├── requirements.txt   # Dependências
└── .env.example       # Template de variáveis de ambiente
```
