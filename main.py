# main.py
from data_generator import generate_mock_data
from reconciliation import run_reconciliation
from forecasting import run_liquidity_forecast

if __name__ == "__main__":
    print("--- Step 1: Initializing Treasury Data ---")
    generate_mock_data()
    
    print("\n--- Step 2: Running Settlement Reconciliation & Claims Detection ---")
    run_reconciliation()
    
    print("\n--- Step 3: Generating Liquidity Forecasts ---")
    run_liquidity_forecast()
    print("\nTreasuryGuard Pipeline Execution Complete.")