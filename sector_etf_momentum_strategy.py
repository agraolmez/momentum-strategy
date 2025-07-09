import yfinance as yf 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

etfs = ["XLF", "XLK", "XLY", "XLP", "XLE", "XLI", "XLV", "XLU", "XLRE", "XLB", "XLC"]
start_date = "2019-01-01"

price_data = {}
all_dates = pd.DatetimeIndex([])

for etf in etfs: 
    print(f"Downloading data for {etf}...")
    df = yf.download(etf, start=start_date, auto_adjust=True, progress=False)
    if not df.empty:
        price_data[etf] = df[('Close', etf)]
        all_dates = all_dates.union(df.index)

for etf in price_data:
    price_data[etf] = price_data[etf].reindex(all_dates)

price_df = pd.DataFrame(price_data)

monthly_prices = price_df.resample('M').last()
monthly_returns = monthly_prices.pct_change().dropna()

lookback_months = 3 
top_n = 3 

momentum_portfolio = []
momentum_dates = []

for i in range(lookback_months, len(monthly_returns) - 1):
    next_date = monthly_returns.index[i + 1]
    past_returns = monthly_returns.iloc[i - lookback_months:i]
    cumulative_returns = (1 + past_returns).prod() - 1 
    valid_returns = cumulative_returns.dropna()
    top_etfs = valid_returns.sort_values(ascending=False).head(top_n).index 
    next_month_returns = monthly_returns.loc[next_date, top_etfs]
    portfolio_return = next_month_returns.mean()
    momentum_portfolio.append(portfolio_return)
    momentum_dates.append(next_date)

spy = yf.download('SPY', start=start_date, auto_adjust=True, progress=False)
spy_returns = spy['Close'].resample('M').last().pct_change().dropna()
spy_aligned = spy_returns.loc[momentum_dates]

rf = yf.download('^IRX', start=start_date, auto_adjust=True, progress=False)
rf_monthly = rf['Close'].resample('M').last().dropna()
rf_monthly = rf_monthly.loc[momentum_dates] / 100  
rf_monthly = (1 + rf_monthly) ** (1/12) - 1  

performance_df = pd.DataFrame({
    'Momentum': momentum_portfolio,
    'SPY': spy_aligned.squeeze(),
    'RiskFree': rf_monthly.squeeze()
}, index=momentum_dates)

excess_returns = performance_df[['Momentum', 'SPY']].sub(performance_df['RiskFree'], axis=0)

cumulative_returns = (1 + performance_df[['Momentum', 'SPY']]).cumprod()
annualized_return = (1 + performance_df[['Momentum', 'SPY']].mean()) ** 12 - 1
annualized_volatility = performance_df[['Momentum', 'SPY']].std() * np.sqrt(12)
sharpe_ratio = (excess_returns.mean() * 12) / (performance_df[['Momentum', 'SPY']].std() * np.sqrt(12))
max_drawdown = (cumulative_returns / cumulative_returns.cummax() - 1).min()

X = sm.add_constant(performance_df['SPY'])
model = sm.OLS(performance_df['Momentum'], X).fit()
alpha = model.params['const']
beta = model.params['SPY']

print("Annualized Return:\n", annualized_return)
print("\n Annualized Volatility:\n", annualized_volatility)
print("\n Sharpe Ratio (with 3M T-Bill):\n", sharpe_ratio)
print("\n Max Drawdown:\n", max_drawdown)
print(f"\n Alpha: {alpha:.4f}")
print(f" Beta: {beta:.4f}")

plt.figure(figsize=(10, 6))
plt.plot(cumulative_returns.index, cumulative_returns['Momentum'], label='Momentum Strategy')
plt.plot(cumulative_returns.index, cumulative_returns['SPY'], label='SPY')
plt.title('Cumulative Returns: Momentum vs SPY')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

metrics_df = pd.DataFrame({
    'Annualized Return': annualized_return,
    'Annualized Volatility': annualized_volatility,
    'Sharpe Ratio': sharpe_ratio
})
metrics_df.plot(kind='bar', figsize=(10, 6))
plt.title("Performance Metrics: Momentum vs SPY")
plt.ylabel("Value")
plt.xticks(rotation=0)
plt.grid(True)
plt.tight_layout()
plt.show()

