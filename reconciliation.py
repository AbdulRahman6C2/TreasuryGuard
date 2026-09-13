import pandas as pd
import numpy as np

def run_reconciliation():
    # Load datasets
    ledger = pd.read_csv('internal_ledger.csv')
    bank = pd.read_csv('bank_statement.csv')
    
    # Convert date columns to datetime objects
    ledger['Expected_Value_Date'] = pd.to_datetime(ledger['Expected_Value_Date'])
    bank['Actual_Settlement_Date'] = pd.to_datetime(bank['Actual_Settlement_Date'])
    
    # Merge datasets on Transaction_ID to find matches and discrepancies
    merged = pd.merge(ledger, bank, on=['Transaction_ID', 'Account_ID', 'Amount', 'Currency', 'Payment_Rail'], how='outer', indicator=True)
    
    # 1. Flag Missing Settlements (Exists in Ledger, missing in Bank Statement)
    missing_settlements = merged[merged['_merge'] == 'left_only'].copy()
    missing_settlements['Exception_Type'] = 'Missing Settlement / Unmatched'
    
    # For matched records, check for Value-Date Breaks (Delayed Settlements)
    matched = merged[merged['_merge'] == 'both'].copy()
    
    # Reload matching rows to evaluate date differences cleanly
    clean_matched = pd.merge(ledger, bank, on='Transaction_ID', suffixes=('_Ledger', '_Bank'))
    clean_matched['Expected_Value_Date'] = pd.to_datetime(clean_matched['Expected_Value_Date'])
    clean_matched['Actual_Settlement_Date'] = pd.to_datetime(clean_matched['Actual_Settlement_Date'])
    
    # Calculate Delay in Days
    clean_matched['Delay_Days'] = (clean_matched['Actual_Settlement_Date'] - clean_matched['Expected_Value_Date']).dt.days
    
    # Filter records where a value-date break occurred (Delay > 0 days)
    value_date_breaks = clean_matched[clean_matched['Delay_Days'] > 0].copy()
    value_date_breaks['Exception_Type'] = 'Value-Date Break (Delayed)'
    
    # Calculate simple economic exposure / carrying cost (Assuming an annualized rate of 5% for delayed capital)
    annual_interest_rate = 0.05
    value_date_breaks['Economic_Impact'] = (
        value_date_breaks['Amount_Ledger'] * (annual_interest_rate / 365) * value_date_breaks['Delay_Days']
    ).round(2)
    
    # Export exception reports for audit & operations review
    value_date_breaks.to_csv('exceptions_value_date_breaks.csv', index=False)
    missing_settlements.to_csv('exceptions_missing_settlements.csv', index=False)
    
    print("Reconciliation complete.")
    print(f"Total Transactions Processed: {len(ledger)}")
    print(f"Value-Date Breaks Flagged: {len(value_date_breaks)}")
    print(f"Missing Settlements Flagged: {len(missing_settlements)}")

if __name__ == "__main__":
    run_reconciliation()