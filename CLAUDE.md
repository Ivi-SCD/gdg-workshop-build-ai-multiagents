# Workshop: Do 0 ao Multi-Agent com Google ADK

## Contexto
Workshop do GDG Recife (9 de maio de 2026). Os participantes seguem os blocos em /docs (BLOCO-1.md a BLOCO-4.md) para construir um sistema multi-agent de análise de investimentos usando Google ADK.

## Stack
- Python 3.12+
- Google ADK (google-adk)
- Google Generative AI SDK (google-genai)
- yfinance (cotações de ações via Yahoo Finance)
- Google Sheets API (gspread + google-auth)

## Estrutura
```
/docs/BLOCO-*.md       — guias passo a passo do workshop
/agents/               — código dos agentes (AGENTS_DIR para adk web)
/agents/tools/         — ferramentas (tools) compartilhadas entre agentes
/agents/data/          — dados para RAG
main.py                — entrypoint do sistema multi-agent
```

**Importante**: `tools/` e `data/` ficam DENTRO de `agents/` porque o ADK adiciona `agents/` ao `sys.path` quando roda `adk web agents/`. Isso garante que imports como `from tools.rag_tool import ...` funcionem.

## Convenções
- Toda config sensível vai em `.env` (nunca commitar keys)
- Código e comentários em português quando didático, nomes de variáveis/funções em inglês
- Cada bloco do workshop é autocontido — o aluno pode rodar o código ao final de cada bloco
- Modelo padrão: gemini-2.5-flash (barato e rápido para workshop)

## Comandos
```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Testar agentes via interface web
adk web agents/

# Rodar sistema completo via CLI
python main.py
```

## Agentes do Sistema
1. **Perfil de Investidor** (Bloco 1) — avalia o perfil de risco do usuário
2. **RAG** (Bloco 2) — busca em base de conhecimento sobre investimentos
3. **Mercado** (Bloco 3) — consulta yfinance, câmbio e Selic em tempo real
4. **Relatório** (Bloco 3) — gera relatório consolidado e exporta para Google Sheets
5. **Orquestrador** (Bloco 4) — coordena todos os agentes acima
