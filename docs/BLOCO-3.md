# Bloco 3 — Agentes Especializados: RAG, Perfil e Mercado

Neste bloco vamos construir os três agentes especializados que formam o núcleo do nosso sistema.

## 3.1 Agente de RAG (Retrieval-Augmented Generation)

Este agente busca informações em uma base de conhecimento local sobre investimentos.

### Passo 1 — Criar a base de conhecimento

```bash
mkdir -p data
```

Crie o arquivo com conteúdo educacional:

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
]
```

### Passo 2 — Criar a tool de busca

```python
# tools/rag_tool.py

from data.knowledge_base import KNOWLEDGE_BASE


def search_knowledge_base(query: str) -> dict:
    """Busca informações na base de conhecimento sobre investimentos.

    Args:
        query: Termo ou pergunta para buscar na base de conhecimento.

    Returns:
        dict com os resultados encontrados.
    """
    query_lower = query.lower()
    results = []

    for item in KNOWLEDGE_BASE:
        if (query_lower in item["topic"].lower()
                or query_lower in item["content"].lower()):
            results.append({
                "topic": item["topic"],
                "content": item["content"].strip(),
            })

    if not results:
        return {"message": "Nenhum resultado encontrado.", "results": []}

    return {"message": f"{len(results)} resultado(s) encontrado(s).", "results": results}
```

### Passo 3 — Criar o agente de RAG

```bash
mkdir -p agents/rag_agent
touch agents/rag_agent/__init__.py
touch agents/rag_agent/agent.py
touch data/__init__.py
touch tools/__init__.py
```

```python
# agents/rag_agent/agent.py

from google.adk.agents import Agent
from tools.rag_tool import search_knowledge_base

rag_agent = Agent(
    name="rag_agent",
    model="gemini-2.0-flash",
    description="Agente especializado em buscar informações sobre investimentos na base de conhecimento.",
    instruction="""
    Você é um agente de RAG especializado em investimentos.
    Sempre use a ferramenta search_knowledge_base para buscar informações antes de responder.
    Baseie suas respostas nos dados retornados pela busca.
    Se não encontrar informações na base, diga que não tem essa informação disponível.
    Responda de forma educacional e clara.
    """,
    tools=[search_knowledge_base],
)
```

```python
# agents/rag_agent/__init__.py

from .agent import rag_agent

root_agent = rag_agent
```

---

## 3.2 Agente de Perfil de Investidor

Este agente avalia o perfil de risco do usuário através de perguntas.

### Passo 1 — Criar o agente

```bash
mkdir -p agents/profile_agent
touch agents/profile_agent/__init__.py
touch agents/profile_agent/agent.py
```

```python
# agents/profile_agent/agent.py

from google.adk.agents import Agent


def classify_profile(
    risk_tolerance: str,
    investment_horizon: str,
    experience: str,
    objective: str,
) -> dict:
    """Classifica o perfil do investidor com base nas respostas.

    Args:
        risk_tolerance: Tolerância a risco (baixa, media, alta).
        investment_horizon: Horizonte de investimento (curto, medio, longo).
        experience: Experiência com investimentos (nenhuma, pouca, moderada, muita).
        objective: Objetivo principal (preservar_capital, renda, crescimento, especulacao).

    Returns:
        dict com o perfil classificado e recomendações.
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
        "profile": profile,
        "score": score,
        "recommended_allocation": allocation,
        "risk_tolerance": risk_tolerance,
        "investment_horizon": investment_horizon,
    }


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

    Faça as perguntas de forma conversacional e amigável.
    Quando tiver todas as respostas, use a ferramenta classify_profile para classificar.
    Apresente o resultado de forma clara e explique o que cada perfil significa.
    """,
    tools=[classify_profile],
)
```

```python
# agents/profile_agent/__init__.py

from .agent import profile_agent

root_agent = profile_agent
```

---

## 3.3 Agente de Mercado

Este agente consulta APIs públicas para obter dados de mercado em tempo real.

### Passo 1 — Criar as tools de mercado

```python
# tools/market_tools.py

import requests


def get_stock_quote(ticker: str) -> dict:
    """Busca a cotação atual de uma ação na B3.

    Args:
        ticker: Código da ação (ex: PETR4, VALE3, ITUB4).

    Returns:
        dict com dados da cotação.
    """
    try:
        url = f"https://brapi.dev/api/quote/{ticker.upper()}"
        response = requests.get(url, timeout=10)
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                "ticker": result.get("symbol", ticker),
                "name": result.get("shortName", "N/A"),
                "price": result.get("regularMarketPrice", "N/A"),
                "change_percent": result.get("regularMarketChangePercent", "N/A"),
                "market_cap": result.get("marketCap", "N/A"),
                "currency": result.get("currency", "BRL"),
            }
        return {"error": f"Ticker {ticker} não encontrado."}
    except Exception as e:
        return {"error": f"Erro ao buscar cotação: {str(e)}"}


def get_currency_rate(currency_pair: str) -> dict:
    """Busca a cotação atual de um par de moedas.

    Args:
        currency_pair: Par de moedas (ex: USD-BRL, EUR-BRL, BTC-BRL).

    Returns:
        dict com dados da cotação do câmbio.
    """
    try:
        url = f"https://economia.awesomeapi.com.br/json/last/{currency_pair.upper()}"
        response = requests.get(url, timeout=10)
        data = response.json()

        key = currency_pair.replace("-", "")
        if key in data:
            result = data[key]
            return {
                "pair": currency_pair,
                "name": result.get("name", "N/A"),
                "bid": result.get("bid", "N/A"),
                "ask": result.get("ask", "N/A"),
                "variation": result.get("pctChange", "N/A"),
                "timestamp": result.get("create_date", "N/A"),
            }
        return {"error": f"Par {currency_pair} não encontrado."}
    except Exception as e:
        return {"error": f"Erro ao buscar câmbio: {str(e)}"}


def get_selic_rate() -> dict:
    """Busca a taxa Selic atual do Banco Central do Brasil.

    Returns:
        dict com a taxa Selic atual.
    """
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data:
            return {
                "taxa_selic": data[0].get("valor", "N/A"),
                "data": data[0].get("data", "N/A"),
                "descricao": "Taxa Selic Meta (% a.a.)",
            }
        return {"error": "Dados da Selic não disponíveis."}
    except Exception as e:
        return {"error": f"Erro ao buscar Selic: {str(e)}"}
```

### Passo 2 — Criar o agente de mercado

```bash
mkdir -p agents/market_agent
touch agents/market_agent/__init__.py
touch agents/market_agent/agent.py
```

```python
# agents/market_agent/agent.py

from google.adk.agents import Agent
from tools.market_tools import get_stock_quote, get_currency_rate, get_selic_rate

market_agent = Agent(
    name="market_agent",
    model="gemini-2.0-flash",
    description="Agente que consulta dados de mercado em tempo real: ações, câmbio e taxas.",
    instruction="""
    Você é um agente especializado em dados de mercado financeiro brasileiro.

    Suas ferramentas:
    - get_stock_quote: busca cotação de ações da B3 (ex: PETR4, VALE3)
    - get_currency_rate: busca cotação de câmbio (ex: USD-BRL, EUR-BRL)
    - get_selic_rate: busca a taxa Selic atual

    Use as ferramentas sempre que o usuário perguntar sobre cotações, preços ou taxas.
    Apresente os dados de forma clara e organizada.
    Lembre que os dados são informativos e não constituem recomendação de investimento.
    """,
    tools=[get_stock_quote, get_currency_rate, get_selic_rate],
)
```

```python
# agents/market_agent/__init__.py

from .agent import market_agent

root_agent = market_agent
```

---

## 3.4 Testando os agentes

Teste cada agente individualmente:

```bash
# Testar todos via interface web
adk web agents/
```

No navegador, selecione cada agente e teste:

- **rag_agent**: "O que é tesouro direto?"
- **profile_agent**: "Quero descobrir meu perfil de investidor"
- **market_agent**: "Qual o preço da PETR4 hoje?"

## 3.5 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| RAG | Retrieval-Augmented Generation — combina busca + geração |
| Tools com APIs | Funções que chamam APIs externas para dados em tempo real |
| Agentes especializados | Cada agente tem um domínio específico de conhecimento |
| `description` | Usado pelo orquestrador para decidir qual agente chamar |

No próximo bloco vamos construir o agente de relatório. Vamos para o [Bloco 4](BLOCO-4.md).
