import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_stock_data(tickers, period="1y"):
    data = {}
    for ticker in tickers:
        stock = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if not stock.empty:
            close = stock['Close']
            if hasattr(close, 'squeeze'):
                close = close.squeeze()
            data[ticker] = close
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)

def calculate_returns(price_data):
    return price_data.pct_change().dropna()

def calculate_portfolio_returns(returns, weights):
    weights = np.array(weights)
    weights = weights / weights.sum()
    return returns.dot(weights)

def calculate_sharpe_ratio(portfolio_returns, risk_free_rate=0.06):
    excess_returns = portfolio_returns - (risk_free_rate / 252)
    sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252)
    return round(float(sharpe), 2)

def calculate_var(portfolio_returns, confidence=0.95):
    var = np.percentile(portfolio_returns, (1 - confidence) * 100)
    return round(float(var) * 100, 2)

def calculate_volatility(returns):
    annual_vol = returns.std() * np.sqrt(252) * 100
    return {ticker: round(float(vol), 2) for ticker, vol in annual_vol.items()}

def calculate_correlation(returns):
    return returns.corr().round(2)

def run_analysis(tickers, weights):
    price_data = get_stock_data(tickers)

    if price_data.empty:
        return {"error": "Could not fetch stock data. Check your tickers."}

    missing = [t for t in tickers if t not in price_data.columns]
    if missing:
        return {"error": f"Could not find data for: {', '.join(missing)}"}

    returns = calculate_returns(price_data)
    portfolio_returns = calculate_portfolio_returns(returns, weights)

    cumulative = (1 + portfolio_returns).cumprod()
    cumulative_pct = ((cumulative - 1) * 100).round(2)

    result = {
        "sharpe_ratio": calculate_sharpe_ratio(portfolio_returns),
        "var_95": calculate_var(portfolio_returns),
        "volatility": calculate_volatility(returns),
        "correlation": calculate_correlation(returns).to_dict(),
        "cumulative_returns": {
            "dates": cumulative_pct.index.strftime('%Y-%m-%d').tolist(),
            "values": cumulative_pct.tolist()
        },
        "tickers": tickers
    }

    return result