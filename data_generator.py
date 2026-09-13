import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data():
    np.random.seed(42)
    num_records = 100
    
    start_date = datetime.now() - timedelta(days=30)
    dates = [start_date + timedelta(days=np.random.randint(0, 30)) for _ in range(num_records)]
    
    # Generate Internal Ledger (Booked Transactions)
    ledger_df = pd.DataFrame({
        'Transaction_ID': [f"TXN-{1000 + i}" for i in range(num_records)],
        'Account_ID': np.random.choice(['ACC-NYC-01', 'ACC-LDN-02', 'ACC-HYD-03'], size=num_records),
        'Expected_Value_Date': dates,
        'Amount': np.round(np.random.uniform(10000, 500000, size=num_records), 2),
        'Currency': 'USD',
        'Payment_Rail': np.random.choice(['SWIFT', 'ACH', 'Wire'], size=num_records)
    })
    
    # Generate Bank Statements (Introduce discrepancies, delays, and missing legs)
    bank_df = ledger_df.copy()
    
    # Introduce value-date shifts for 15% of records (simulating delayed settlements)
    delay_indices = np.random.choice(num_records, size=int(num_records * 0.15), replace=False)
    for idx in delay_indices:
        bank_df.loc[idx, 'Expected_Value_Date'] += timedelta(days=np.random.randint(1, 4))
        
    # Drop 5% of bank records entirely (simulating missing statement legs)
    drop_indices = np.random.choice(num_records, size=int(num_records * 0.05), replace=False)
    bank_df = bank_df.drop(drop_indices).reset_index(drop=True)
    
    # Rename date column in bank data to represent actual settlement date
    bank_df = bank_df.rename(columns={'Expected_Value_Date': 'Actual_Settlement_Date'})
    
    # Save to CSV for testing
    ledger_df.to_csv('internal_ledger.csv', index=False)
    bank_df.to_csv('bank_statement.csv', index=False)
    print("Mock data generated successfully: internal_ledger.csv & bank_statement.csv created.")

if __name__ == "__main__":
    generate_mock_data()