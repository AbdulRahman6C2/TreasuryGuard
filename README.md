# TreasuryGuard: Automated Settlement Reconciliation & Cash Flow Risk Engine

TreasuryGuard is an end-to-end Python application designed to simulate and automate core institutional treasury operations. Built to address high-volume transaction processing, the system ingests payment ledgers and bank statement feeds, executes automated reconciliations, flags value-date breaks (claims triggers), calculates economic exposure, and models short-term liquidity risks using time-series forecasting.

## Key Features

* **Automated Data Reconciliation:** Cross-examines internal transaction ledgers against bank statement feeds to instantly identify matching legs, discrepancies, and processing exceptions across payment rails (SWIFT, ACH, Wire).
* **Claims & Exception Detection:** Programmatically flags missing settlement legs and value-date breaks (delayed settlements).
* **Economic Impact Modeling:** Calculates carrying-cost exposure and financial impact using standard annualized interest formulas for delayed transactions.
* **Liquidity Risk Forecasting:** Implements an ARIMA statistical time-series model to analyze historical daily cash flows and project short-term liquidity fluctuations.
* **Audit-Ready Reporting:** Generates clean, structured exception logs and forecast outputs for operational review and risk governance.

---

## Project Architecture

```text
TreasuryGuard/
│
├── data_generator.py          # Simulates realistic institutional SWIFT/wire transaction logs & bank statements
├── reconciliation.py          # Executes ledger matching, flags value-date breaks & calculates economic exposure
├── forecasting.py             # Applies ARIMA time-series modeling for daily cash flow and liquidity forecasting
├── main.py                    # Master orchestrator script running the end-to-end pipeline
├── internal_ledger.csv        # Sample internal book of record transactions
├── bank_statement.csv         # Sample bank statement feed with simulated delays and missing legs
├── requirements.txt           # Project python package dependencies
└── .gitignore                 # Excludes virtual environments and cached files