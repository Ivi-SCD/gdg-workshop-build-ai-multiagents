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