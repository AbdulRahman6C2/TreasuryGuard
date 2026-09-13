import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

def run_liquidity_forecast():
    # Load ledger data
    ledger = pd.read_csv('internal_ledger.csv')
    ledger['Expected_Value_Date'] = pd.to_datetime(ledger['Expected_Value_Date'])
    
    # Aggregate daily cash flows to create a time series
    daily_cash = ledger.groupby('Expected_Value_Date')['Amount'].sum().reset_index()
    daily_cash = daily_cash.sort_values('Expected_Value_Date')
    daily_cash.set_index('Expected_Value_Date', inplace=True)
    
    # Ensure a complete daily frequency index for time-series modeling
    daily_cash = daily_cash.asfreq('D', fill_value=0)
    
    # Fit a simple ARIMA model to forecast short-term cash flow volatility
    try:
        model = ARIMA(daily_cash['Amount'], order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=5)
        print("Liquidity Risk Forecast (Next 5 Days):")
        print(forecast)
    except Exception as e:
        print("Forecasting note: Data points span varied intervals; check data density. Moving average fallback applied.")
        rolling_avg = daily_cash['Amount'].rolling(window=3).mean().iloc[-1]
        print(f"Estimated Projected Daily Cash Flow Baseline: ${rolling_avg:,.2f}")

if __name__ == "__main__":
    run_liquidity_forecast()