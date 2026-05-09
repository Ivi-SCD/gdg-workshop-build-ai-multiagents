# Bloco 3 — Agente de Mercado + Agente de Relatório

Neste bloco vamos construir dois agentes: um que consulta dados de mercado em tempo real via APIs públicas e outro que gera relatórios exportados para Google Sheets.

---

## Parte 1: Agente de Mercado

### 3.1 APIs que vamos usar

| API | Dados | Key? |
|-----|-------|------|
| **yfinance** | Cotação de ações (B3 e global) | Não |
| **AwesomeAPI** | Cotação de câmbio (USD, EUR, BTC) | Não |
| **Banco Central (BCB)** | Taxa Selic | Não |

Todas são gratuitas e não precisam de cadastro — perfeitas para o workshop.

### 3.2 Criando as tools de mercado

```bash
mkdir -p agents/market_agent/tools
```

```python
# agents/market_agent/tools/market_tools.py

import requests
import yfinance as yf


def get_stock_quote(ticker: str) -> dict:
    """Busca a cotação atual de uma ação brasileira ou internacional.

    Args:
        ticker: Código da ação. Para B3 use o sufixo .SA (ex: PETR4.SA, VALE3.SA, ITUB4.SA).
               Para ações americanas use o ticker direto (ex: AAPL, GOOGL, MSFT).

    Returns:
        dict com dados da cotação incluindo preço, variação e volume.
    """
    try:
        stock = yf.Ticker(ticker.upper())
        info = stock.info

        if not info or "regularMarketPrice" not in info:
            return {"error": f"Ticker {ticker} não encontrado. Para ações da B3, use o sufixo .SA (ex: PETR4.SA)."}

        return {
            "ticker": info.get("symbol", ticker),
            "nome": info.get("shortName", "N/A"),
            "preco": info.get("regularMarketPrice", "N/A"),
            "variacao_percentual": info.get("regularMarketChangePercent", "N/A"),
            "abertura": info.get("regularMarketOpen", "N/A"),
            "maxima": info.get("regularMarketDayHigh", "N/A"),
            "minima": info.get("regularMarketDayLow", "N/A"),
            "volume": info.get("regularMarketVolume", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "moeda": info.get("currency", "N/A"),
        }
    except Exception as e:
        return {"error": f"Erro ao buscar cotação: {str(e)}"}


def get_stock_history(ticker: str, period: str) -> dict:
    """Busca o histórico de preços de uma ação.

    Args:
        ticker: Código da ação (ex: PETR4.SA, VALE3.SA, AAPL).
        period: Período do histórico (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y).

    Returns:
        dict com o histórico de preços (últimos registros).
    """
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period=period)

        if hist.empty:
            return {"error": f"Sem dados históricos para {ticker} no período {period}."}

        records = []
        for date, row in hist.tail(10).iterrows():
            records.append({
                "data": date.strftime("%Y-%m-%d"),
                "abertura": round(row["Open"], 2),
                "maxima": round(row["High"], 2),
                "minima": round(row["Low"], 2),
                "fechamento": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            })

        return {
            "ticker": ticker.upper(),
            "periodo": period,
            "total_registros": len(hist),
            "ultimos_registros": records,
        }
    except Exception as e:
        return {"error": f"Erro ao buscar histórico: {str(e)}"}


def get_currency_rate(currency_pair: str) -> dict:
    """Busca a cotação atual de um par de moedas.

    Args:
        currency_pair: Par de moedas (ex: USD-BRL, EUR-BRL, BTC-BRL, GBP-BRL).

    Returns:
        dict com dados da cotação do câmbio.
    """
    try:
        url = f"https://economia.awesomeapi.com.br/json/last/{currency_pair.upper()}"
        response = requests.get(url, timeout=10)
        data = response.json()

        key = currency_pair.upper().replace("-", "")
        if key in data:
            result = data[key]
            return {
                "par": currency_pair,
                "nome": result.get("name", "N/A"),
                "compra": result.get("bid", "N/A"),
                "venda": result.get("ask", "N/A"),
                "variacao": result.get("pctChange", "N/A"),
                "maxima": result.get("high", "N/A"),
                "minima": result.get("low", "N/A"),
                "timestamp": result.get("create_date", "N/A"),
            }
        return {"error": f"Par {currency_pair} não encontrado."}
    except Exception as e:
        return {"error": f"Erro ao buscar câmbio: {str(e)}"}


def get_selic_rate() -> dict:
    """Busca a taxa Selic atual do Banco Central do Brasil.

    Returns:
        dict com a taxa Selic atual e data de referência.
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

### 3.3 Criando o agente de mercado

```python
# agents/market_agent/agent.py

from google.adk.agents import Agent
from .tools.market_tools import get_stock_quote, get_stock_history, get_currency_rate, get_selic_rate

market_agent = Agent(
    name="market_agent",
    model="gemini-2.5-flash",
    description="Agente que consulta dados de mercado em tempo real: cotações de ações, câmbio e taxas de juros.",
    instruction="""
    Você é um agente especializado em dados de mercado financeiro.

    Suas ferramentas:
    - get_stock_quote: cotação atual de ações (B3 com sufixo .SA, ex: PETR4.SA)
    - get_stock_history: histórico de preços (períodos: 1d, 5d, 1mo, 3mo, 6mo, 1y)
    - get_currency_rate: cotação de câmbio (ex: USD-BRL, EUR-BRL, BTC-BRL)
    - get_selic_rate: taxa Selic atual do Banco Central

    REGRAS:
    - Use as ferramentas SEMPRE que o usuário perguntar sobre cotações, preços ou taxas
    - Para ações da B3, lembre o usuário do formato com .SA se ele esquecer
    - Apresente os dados de forma clara e organizada
    - Inclua a data/hora dos dados quando disponível
    - Lembre que os dados são informativos e não constituem recomendação de investimento
    """,
    tools=[get_stock_quote, get_stock_history, get_currency_rate, get_selic_rate],
)
```

```python
# agents/market_agent/__init__.py

from .agent import market_agent

root_agent = market_agent
```

### 3.4 Testando o agente de mercado

```bash
adk web agents/
```

Selecione **market_agent** e teste:

| Pergunta | Tool chamada |
|----------|-------------|
| "Qual o preço da PETR4?" | `get_stock_quote("PETR4.SA")` |
| "Histórico da VALE3 no último mês" | `get_stock_history("VALE3.SA", "1mo")` |
| "Quanto tá o dólar?" | `get_currency_rate("USD-BRL")` |
| "Qual a Selic atual?" | `get_selic_rate()` |
| "Compara PETR4 e VALE3" | Duas chamadas de `get_stock_quote` |

---

## Parte 2: Agente de Relatório + Google Sheets

### 3.5 Configurando o Google Sheets API

#### Passo 1 — Criar uma Service Account

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Selecione seu projeto
3. Selecione o Menu Hambúrguer
4. Vá em **APIs & Services > Enable APIs** e habilite:
   - **Google Sheets API**
   - **Google Drive API**
5. Vá em **APIs & Services > Credentials**
6. Clique em **Create Credentials > Service Account**
7. Dê um nome (ex: `workshop-sheets`) e clique em **Done**
8. Clique na service account > **Keys > Add Key > Create new key > JSON**
9. Salve o arquivo como `credentials.json` na raiz do projeto

#### Passo 2 — Compartilhar a planilha

1. Crie uma nova planilha no Google Sheets
2. Copie o ID da URL: `https://docs.google.com/spreadsheets/d/{ESTE_ID}/edit`
3. Compartilhe com o email da service account (campo `client_email` no JSON) como **Editor**

#### Passo 3 — Atualizar o .env

```bash
# Adicione ao .env
GOOGLE_SHEETS_CREDENTIALS=credentials.json
GOOGLE_SHEETS_SPREADSHEET_ID=cole-o-id-da-sua-planilha-aqui
```

### 3.6 Criando a tool do Google Sheets

```bash
mkdir -p agents/report_agent/tools
```

```python
# agents/report_agent/tools/sheets_tools.py

import os
from datetime import datetime

import gspread
from google.oauth2.service_account import Credentials


def _get_sheets_client():
    """Cria o cliente autenticado do Google Sheets."""
    creds_file = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "credentials.json")
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    return gspread.authorize(creds)


def export_report_to_sheets(
    report_title: str,
    investor_profile: str,
    recommended_allocation: str,
    market_data: str,
    analysis_summary: str,
) -> dict:
    """Exporta um relatório de análise de investimentos para o Google Sheets.

    Args:
        report_title: Título do relatório.
        investor_profile: Perfil do investidor (Conservador, Moderado, Arrojado, Agressivo).
        recommended_allocation: Alocação recomendada de ativos.
        market_data: Dados de mercado coletados (texto formatado).
        analysis_summary: Resumo da análise e recomendações.

    Returns:
        dict com status da exportação e link da planilha.
    """
    try:
        client = _get_sheets_client()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if not spreadsheet_id:
            return {"error": "GOOGLE_SHEETS_SPREADSHEET_ID não configurado no .env"}

        spreadsheet = client.open_by_key(spreadsheet_id)

        sheet_name = f"Relatório {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=20, cols=5)

        worksheet.update("A1:B1", [["Relatório de Investimentos", ""]])
        worksheet.update("A2:B2", [["Título", report_title]])
        worksheet.update("A3:B3", [["Data", datetime.now().strftime("%d/%m/%Y %H:%M")]])
        worksheet.update("A4:B4", [["Perfil do Investidor", investor_profile]])
        worksheet.update("A5:B5", [["Alocação Recomendada", recommended_allocation]])
        worksheet.update("A7:A7", [["Dados de Mercado"]])
        worksheet.update("A8:A8", [[market_data]])
        worksheet.update("A10:A10", [["Análise e Recomendações"]])
        worksheet.update("A11:A11", [[analysis_summary]])

        worksheet.format("A1:B1", {"textFormat": {"bold": True, "fontSize": 14}})
        worksheet.format("A2:A11", {"textFormat": {"bold": True}})

        return {
            "status": "success",
            "message": f"Relatório exportado para a aba '{sheet_name}'.",
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
            "sheet_name": sheet_name,
        }
    except Exception as e:
        return {"error": f"Erro ao exportar: {str(e)}"}


def list_reports() -> dict:
    """Lista todos os relatórios existentes na planilha do Google Sheets.

    Returns:
        dict com a lista de abas/relatórios existentes na planilha.
    """
    try:
        client = _get_sheets_client()
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID")

        if not spreadsheet_id:
            return {"error": "GOOGLE_SHEETS_SPREADSHEET_ID não configurado no .env"}

        spreadsheet = client.open_by_key(spreadsheet_id)
        sheets = [ws.title for ws in spreadsheet.worksheets()]

        return {
            "total": len(sheets),
            "relatorios": sheets,
            "spreadsheet_url": f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}",
        }
    except Exception as e:
        return {"error": f"Erro ao listar relatórios: {str(e)}"}
```

### 3.7 Criando o agente de relatório

```python
# agents/report_agent/agent.py

from google.adk.agents import Agent
from .tools.sheets_tools import export_report_to_sheets, list_reports

report_agent = Agent(
    name="report_agent",
    model="gemini-2.5-flash",
    description="Agente que gera relatórios consolidados de investimentos e exporta para Google Sheets.",
    instruction="""
    Você é um agente especializado em gerar relatórios de investimentos.

    Seu trabalho é:
    1. Receber dados de análise (perfil do investidor, dados de mercado, recomendações)
    2. Organizar as informações de forma clara
    3. Exportar para Google Sheets usando export_report_to_sheets
    4. Listar relatórios existentes com list_reports quando solicitado

    Ao gerar o relatório:
    - Use um título descritivo
    - Organize os dados de mercado de forma legível
    - Escreva um resumo claro e acionável
    - Inclua o disclaimer: as informações são educacionais e não constituem recomendação

    Ao final, compartilhe o link da planilha com o usuário.
    """,
    tools=[export_report_to_sheets, list_reports],
)
```

```python
# agents/report_agent/__init__.py

from .agent import report_agent

root_agent = report_agent
```

### 3.8 Testando o agente de relatório

```bash
adk web agents/
```

Selecione **report_agent** e teste:

- "Gere um relatório para investidor moderado com PETR4 a R$38,50 e dólar a R$5,20"
- "Liste os relatórios existentes"

Se o Google Sheets não estiver configurado, o agente retornará um erro claro — isso é esperado caso você não tenha feito o setup da service account.

## 3.9 Conceitos-chave aprendidos

| Conceito | Descrição |
|----------|-----------|
| yfinance | Biblioteca para acessar dados do Yahoo Finance sem API key |
| APIs públicas | AwesomeAPI (câmbio) e BCB (Selic) para dados em tempo real |
| Service Account | Credencial para acessar APIs Google programaticamente |
| Google Sheets API | Permite criar e escrever planilhas via código |
| Tools com side effects | Ferramentas que criam artefatos externos |

No próximo bloco vamos juntar todos os agentes com o orquestrador. Vamos para o [Bloco 4](BLOCO-4.md).
