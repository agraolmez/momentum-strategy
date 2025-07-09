This project implements a monthly momentum-based investment strategy using 11 S&P 500 sector ETFs.

- Methodology:
  
Lookback Period: 3 months
Selection Rule: Top 3 ETFs with the highest cumulative return
Holding Period: 1 month, equal-weighted
Benchmark: SPY (S&P 500 ETF)
Risk-Free Rate: 3-month T-Bill (^IRX)

- Performance Metrics:
  
Metric	Momentum	SPY
Annualized Return	13.5%	17.5%
Annualized Volatility	16.7%	17.1%
Sharpe Ratio (3M T-Bill)	0.61	0.80
Max Drawdown	-18.3%	-23.9%
Alpha	-0.0003	—
Beta	0.81	1.00

- Interpretation:
  
SPY outperformed in absolute return.
Momentum had a lower drawdown and a lower beta (less sensitive to the market).
Sharpe ratio is slightly worse, indicating a less efficient risk-return tradeoff for this period.

- Tools Used:
  
Python
yfinance
pandas
matplotlib
statsmodels
