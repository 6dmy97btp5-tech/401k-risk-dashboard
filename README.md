# 401(k) Alternative Investment Risk Analysis Dashboard

> An interactive financial dashboard for analyzing alternative investment risk exposure within 401(k) portfolios — built with Python, Streamlit, Pandas, and Plotly.

> 🚧 **Status: In Development**

-----

## Overview

This dashboard was built in response to evolving DOL policy allowing alternative investments — including private equity, hedge funds, and real assets — inside 401(k) plans. As these products become more accessible to retail retirement investors, the need for clear, accessible risk analysis tools becomes critical.

This tool gives financial professionals and investors a structured way to analyze, visualize, and compare the risk profile of alternative investments within a 401(k) portfolio context.

-----

## Features (Planned & In Progress)

- **Live Market Data Pull**
  Fetches current and historical pricing data via `yfinance` for equities, ETFs, and alternative investment proxies.
- **Risk Metrics Dashboard**
  Calculates and displays:
  - Volatility (Standard Deviation)
  - Sharpe Ratio
  - Max Drawdown
  - Correlation Matrix
- **Portfolio Allocation Simulator**
  Interactive sliders to model different allocation weights across traditional and alternative asset classes.
- **Visual Analytics**
  Interactive charts powered by Plotly:
  - Risk/Return scatter plots
  - Correlation heatmaps
  - Historical performance overlays
  - Drawdown visualizations
- **Alternative Investment Coverage**
  - Private Equity proxies (PSP, PEX)
  - Real Assets / REITs (VNQ, SCHH)
  - Commodities (GLD, DJP)
  - Hedge Fund proxies (HFND, WTMF)
  - Infrastructure (IFRA, PAVE)

-----

## Tech Stack

|Tool     |Purpose                   |
|---------|--------------------------|
|Python   |Core language             |
|Streamlit|Interactive web dashboard |
|Pandas   |Data manipulation         |
|Plotly   |Interactive visualizations|
|yfinance |Live market data          |

-----

## Project Background

This dashboard is part of an ongoing effort to build AI-enabled financial infrastructure tools — combining financial services domain expertise with Python-based data tooling. It reflects a broader focus on making complex investment analysis accessible and actionable for financial professionals.

-----

## Development Status

|Feature                      |Status       |
|-----------------------------|-------------|
|Data pull function (yfinance)|🔄 In Progress|
|Risk metrics calculations    |🔄 In Progress|
|Portfolio simulator          |📋 Planned    |
|Plotly visualizations        |📋 Planned    |
|Streamlit deployment         |📋 Planned    |

-----

## Author

**Ravell Greenfield**
Associate Service Consultant — Annuities Trading Department, LPL Financial
FINRA SIE Certified | Series 7 & 63 Candidate

[LinkedIn](https://www.linkedin.com/in/ravell-greenfield-12b3b8207)
[GitHub](https://github.com/6dmy97btp5-tech)

-----

## Disclaimer

This tool is for educational and analytical purposes only. It does not constitute investment advice. All data is sourced from publicly available market data. Past performance is not indicative of future results.