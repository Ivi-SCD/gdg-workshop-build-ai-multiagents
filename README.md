# GDG Recife - Do 0 ao Multi-Agent com Google ADK

Workshop prático onde você vai sair do zero até construir um sistema multi-agent completo para análise de investimentos usando o **Google Agent Development Kit (ADK)**.

## Palestrantes

| Nome | Contato |
|------|---------|
| **Ivisson Alves** | [Linkedin](https://www.linkedin.com/in/ivi-aiengineer/) & [Instagram](https://www.instagram.com/ivii.ai)
| **Giulia Buonafina** | [Linkedin](https://www.linkedin.com/in/giulia-buonafina-019574260/) & [Instagram](https://www.instagram.com/data.giu/)

## O que vamos construir?

Um sistema multi-agent de análise de investimentos composto por:

- **Agente Orquestrador** — recebe perguntas e delega para agentes especializados
- **Agente de RAG** — busca em base de conhecimento sobre investimentos
- **Agente de Perfil de Investidor** — avalia o perfil de risco do usuário
- **Agente de Mercado** — consulta APIs públicas para dados em tempo real
- **Agente de Relatório** — gera relatório consolidado e exporta para Google Sheets

## Pré-requisitos

- Python 3.12+
- Conta Google
- Conta Google Cloud (GCP para Google AI Studio e API Key)
- Git & Github
- Sua IDE Favorita (VS Code, VIM, Bloco de Notas, feel free)

## Setup rápido

```bash
git clone https://github.com/Ivi-SCD/gdg-workshop-build-ai-multiagents.git
cd gdg-workshop-build-ai-multiagents

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

pip install -r requirements.txt

cp .env.example .env
# Edite o .env com sua API Key
```

## Roteiro do Workshop

| Bloco | Tema | Doc | Tempo
|-------|------|-----|-----
| 1 | Google AI Studio — Conceitos e Playground, Google ADK + Primeiro Agente | [BLOCO-1](docs/BLOCO-1.md) | 30min
| 2 | Agente RAG | [BLOCO-2](docs/BLOCO-2.md) | 30min
| 3 | Agente Mercado + Agente Relatório | [BLOCO-3](docs/BLOCO-3.md) | 30min
| 4 | Multi-Agents | [BLOCO-4](docs/BLOCO-4.md) | 30min

## Estrutura do projeto

```
├── agents/                # AGENTS_DIR — cada pasta é um agente
│   ├── orchestrator/      # Agente orquestrador (Bloco 4)
│   ├── profile_agent/     # Agente de perfil de investidor (Bloco 1)
│   ├── rag_agent/         # Agente RAG + tools/ + data/ (Bloco 2)
│   ├── market_agent/      # Agente de mercado + tools/ (Bloco 3)
│   └── report_agent/      # Agente de relatório + tools/ (Bloco 3)
├── docs/                  # Guias passo a passo (BLOCO-*.md)
├── main.py                # Entrypoint do sistema multi-agent
├── requirements.txt       # Dependências
└── .env.example           # Template de variáveis de ambiente
```
