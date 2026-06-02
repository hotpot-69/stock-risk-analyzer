# RiskLens — Stock Portfolio Risk Analyzer

A web application that analyzes the risk profile of any stock portfolio using real market data.

## Features
- Real-time stock data via Yahoo Finance
- Sharpe Ratio — risk-adjusted return metric
- Value at Risk (VaR) at 95% confidence
- Annualised volatility per stock
- Correlation heatmap for diversification analysis
- Supports both Indian (.NS) and US stocks

## Tech Stack
Python, Flask, yfinance, Pandas, NumPy, Plotly

## How to Run
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

