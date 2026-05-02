# Bloco 2 — Agente RAG (Retrieval-Augmented Generation)

Neste bloco vamos construir um agente que busca informações em uma base de conhecimento local sobre investimentos antes de responder.

## 2.1 O que é RAG?

**RAG (Retrieval-Augmented Generation)** é uma técnica que combina:

1. **Retrieval**: buscar informações relevantes em uma base de dados
2. **Augmented**: usar essas informações como contexto
3. **Generation**: gerar uma resposta baseada no contexto encontrado

Isso reduz alucinações e permite que o modelo responda com dados específicos do seu domínio.

```
Pergunta do usuário
        │
        ▼
┌──────────────┐     ┌──────────────────┐
│   Retrieval  │────▶│ Base de           │
│   (busca)    │◀────│ Conhecimento      │
└──────┬───────┘     └──────────────────┘
       │
       ▼
┌──────────────┐
│  Generation  │ ← contexto encontrado + pergunta
│  (Gemini)    │
└──────┬───────┘
       │
       ▼
   Resposta
```

## 2.2 Criando a base de conhecimento

```bash
mkdir -p data
touch data/__init__.py
```

```python
# data/knowledge_base.py

KNOWLEDGE_BASE = [
    {
        "topic": "Renda Fixa",
        "content": """
        Renda fixa são investimentos onde as regras de remuneração são definidas no momento da aplicação.
        Tipos principais: Tesouro Direto (Selic, IPCA+, Prefixado), CDB, LCI, LCA, Debêntures.
        Risco: geralmente baixo, protegido pelo FGC até R$250 mil por CPF por instituição.
        Indicado para: perfil conservador, reserva de emergência, objetivos de curto prazo.
        """,
    },
    {
        "topic": "Renda Variável",
        "content": """
        Renda variável são investimentos onde o retorno não é previsível no momento da aplicação.
        Tipos principais: Ações, FIIs (Fundos Imobiliários), ETFs, BDRs, Criptomoedas.
        Risco: alto, sem garantia do FGC. Preço varia conforme mercado.
        Indicado para: perfil moderado a arrojado, objetivos de longo prazo.
        """,
    },
    {
        "topic": "Fundos de Investimento",
        "content": """
        Fundos são veículos coletivos geridos por um gestor profissional.
        Tipos: Renda Fixa, Multimercado, Ações, Cambial, Imobiliário (FIIs).
        Custos: taxa de administração, taxa de performance, come-cotas.
        Vantagem: diversificação e gestão profissional. Desvantagem: taxas e menos controle.
        """,
    },
    {
        "topic": "Tesouro Direto",
        "content": """
        Programa do governo federal para venda de títulos públicos a pessoas físicas.
        Tesouro Selic: pós-fixado, acompanha a taxa Selic. Ideal para reserva de emergência.
        Tesouro IPCA+: híbrido, paga IPCA + taxa fixa. Protege contra inflação.
        Tesouro Prefixado: taxa definida na compra. Bom quando se espera queda de juros.
        Investimento mínimo: ~R$30. Liquidez: D+1 (Selic) ou mercado secundário.
        """,
    },
    {
        "topic": "Diversificação",
        "content": """
        Estratégia de distribuir investimentos entre diferentes classes de ativos.
        Objetivo: reduzir risco sem necessariamente sacrificar retorno.
        Regra geral: não colocar todos os ovos na mesma cesta.
        Exemplos de alocação: conservador (80% RF, 20% RV), moderado (60/40), arrojado (30/70).
        Rebalanceamento periódico é importante para manter a alocação alvo.
        """,
    },
    {
        "topic": "FIIs - Fundos Imobiliários",
        "content": """
        FIIs são fundos que investem em imóveis ou títulos imobiliários, negociados em bolsa.
        Tipos: tijolo (imóveis físicos), papel (CRIs/CRAs), híbridos, fundos de fundos.
        Vantagem: rendimentos mensais isentos de IR para pessoa física (com condições).
        Risco: vacância, inadimplência, variação de cotas, risco de mercado.
        Indicado para: quem busca renda passiva com exposição ao setor imobiliário.
        """,
    },
    {
        "topic": "Análise Fundamentalista",
        "content": """
        Método de avaliação que analisa os fundamentos econômicos de uma empresa.
        Indicadores principais: P/L (Preço/Lucro), P/VP (Preço/Valor Patrimonial),
        ROE (Retorno sobre Patrimônio), Dividend Yield, Margem Líquida.
        Objetivo: determinar se uma ação está cara ou barata em relação ao seu valor intrínseco.
        Usado por investidores de longo prazo (buy and hold, value investing).
        """,
    },
    {
        "topic": "ETFs",
        "content": """
        ETFs (Exchange Traded Funds) são fundos de índice negociados em bolsa.
        Replicam índices como Ibovespa (BOVA11), S&P 500 (IVVB11), Small Caps (SMAL11).
        Vantagem: diversificação instantânea, baixas taxas de administração, liquidez.
        Desvantagem: não há isenção de IR para vendas até R$20 mil/mês (como ações).
        Ideal para: investidores que querem diversificação com simplicidade.
        """,
    },
]
```

## 2.3 Criando a tool de busca

```bash
mkdir -p tools
touch tools/__init__.py
```

```python
# tools/rag_tool.py

from data.knowledge_base import KNOWLEDGE_BASE


def search_knowledge_base(query: str) -> dict:
    """Busca informações na base de conhecimento sobre investimentos.

    Args:
        query: Termo ou pergunta para buscar na base de conhecimento.

    Returns:
        dict com os resultados encontrados na base.
    """
    query_lower = query.lower()
    results = []

    for item in KNOWLEDGE_BASE:
        topic_match = query_lower in item["topic"].lower()
        content_match = any(
            word in item["content"].lower()
            for word in query_lower.split()
            if len(word) > 3
        )

        if topic_match or content_match:
            results.append({
                "topic": item["topic"],
                "content": item["content"].strip(),
            })

    if not results:
        return {
            "message": "Nenhum resultado encontrado na base de conhecimento.",
            "results": [],
        }

    return {
        "message": f"{len(results)} resultado(s) encontrado(s).",
        "results": results,
    }
```

> **Nota**: essa busca é por keywords. Em produção, usaríamos embeddings + busca vetorial para resultados mais relevantes. Para o workshop, keyword search é suficiente e didático.

## 2.4 Criando o agente de RAG

```bash
mkdir -p agents/rag_agent
touch agents/rag_agent/__init__.py
touch agents/rag_agent/agent.py
```

```python
# agents/rag_agent/agent.py

from google.adk.agents import Agent
from tools.rag_tool import search_knowledge_base

rag_agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash",
    description="Agente especializado em buscar e explicar informações sobre investimentos usando a base de conhecimento.",
    instruction="""
    Você é um agente de RAG especializado em investimentos.

    REGRAS:
    1. SEMPRE use a ferramenta search_knowledge_base antes de responder qualquer pergunta
    2. Baseie suas respostas nos dados retornados pela busca
    3. Se não encontrar informações na base, diga claramente que não tem essa informação disponível
    4. Responda de forma educacional, clara e didática
    5. Pode complementar com explicações, mas o núcleo da resposta deve vir da base
    6. Sempre mencione que suas respostas são educacionais e não constituem recomendação de investimento

    Você é o especialista em conhecimento teórico sobre investimentos do nosso sistema.
    """,
    tools=[search_knowledge_base],
)
```

```python
# agents/rag_agent/__init__.py

from .agent import rag_agent

root_agent = rag_agent
```

## 2.5 Testando o agente

```bash
adk web agents/
```

Selecione **rag_agent** e teste:

| Pergunta | Esperado |
|----------|----------|
| "O que é tesouro direto?" | Busca na base e explica os tipos de título |
| "Me explica sobre FIIs" | Busca fundos imobiliários e detalha |
| "O que são ETFs?" | Retorna informações sobre ETFs |
| "Como funciona a diversificação?" | Explica a estratégia e exemplos de alocação |
| "O que é bitcoin?" | Deve dizer que não encontrou na base |

## 2.6 Como o RAG funciona por baixo

Quando você pergunta "O que é tesouro direto?":

```
1. Agente recebe a pergunta
2. Gemini decide chamar search_knowledge_base(query="tesouro direto")
3. Tool busca na KNOWLEDGE_BASE por matches
4. Retorna: {topic: "Tesouro Direto", content: "Programa do governo..."}
5. Gemini usa esse contexto para gerar a resposta final
6. Usuário recebe uma resposta fundamentada nos dados da base
```

O model **decide sozinho** quando e como chamar a tool — isso é **function calling** em ação.

## 2.7 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| RAG | Busca + contexto + geração — reduz alucinações |
| Knowledge Base | Base de dados com informações do domínio |
| Keyword Search | Busca simples por palavras-chave (produção usa embeddings) |
| Function Calling | O modelo decide quando chamar a tool |
| Grounding | Fundamentar respostas em dados reais |

No próximo bloco vamos construir os agentes de mercado e relatório. Vamos para o [Bloco 3](BLOCO-3.md).
