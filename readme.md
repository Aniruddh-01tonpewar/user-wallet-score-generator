<details><summary>Click to expand the full readme content</summary>

# Wallet Credit Scoring with Aave V2 Transaction Data

## Overview

This project implements a wallet-level credit scoring model using historical transactions from the **Aave V2 DeFi protocol**. The goal is to identify responsible vs. risky behavior based solely on the nature and volume of wallet interactions. Each wallet receives a credit score between **0 and 1000**, indicating its behavioral reliability within the protocol.

---

##  Methodology

###  Modeling Philosophy

The approach classifies each wallet’s transaction as either responsible or risky using **Logistic Regression**, based on encoded action type and transformed transaction amount. It then averages predicted probabilities per wallet to generate a score, scaled to the range [0–1000].

This choice balances interpretability with efficiency, ideal for rapid iteration and extensibility.

---

##  Architecture & Processing Flow

```mermaid
graph TD
    A[Load raw JSON data] --> B[Normalize JSON structure]
    B --> C [Extract: userWallet, actionType, amount]
    C --> D [Convert amount to float]
    D --> E [Apply log1p transformation]
    E --> F [Encode action types into features]
    F --> G [Map target labels: responsible vs risky]
    G --> H [Train Logistic Regression model]
    H --> I [Predict probabilities for each transaction]
    I --> J [Aggregate predictions by wallet]
    J --> K [Scale probabilities to credit score (0–1000)]
    K --> L [Output final wallet-score dictionary]
    
##  Feature Engineering

###  Feature Encoding Table

| Action Type         | Feature Score | Target Label | Description                         |
|---------------------|---------------|--------------|-------------------------------------|
| `Deposit`           | 5             | 1            | Positive behavior; funds supplied   |
| `Repay`             | 3             | 1            | Responsible repayment               |
| `RedeemUnderlying`  | 4             | 1            | Withdrawal after lending            |
| `Borrow`            | 2             | 0            | Liability taken; requires repayment |
| `LiquidationCall`   | 1             | 0            | Risk signal; collateral liquidation |

Amounts are log-transformed using log1p and rounded to 2 decimals to minimize skew and stabilize learning.

## Model Selection

The model used is Logistic Regression due to its:
- Speed and simplicity
- Interpretability for binary classification tasks
- Ability to handle class imbalance via class_weight='balanced'
- Compatibility with numeric, scaled features Solver: liblinear


##  Score Generation Logic

Each transaction is classified with a probability of responsible behavior. 
The final score is computed by:
wallet_scores = df.groupby("wallet")["responsible_prob"].mean()
wallet_scores_scaled = (wallet_scores * 1000).round().astype(int)

##  How to Run

Install dependencies:
pip install pandas numpy scikit-learn
Execute the script:
python wallet_score_generator.py

This one-step script loads the transaction data, processes features, trains the model, scores each wallet, and exports results to wallet_scores.json.

##  Dataset Requirement

Before running the script, please ensure the sample transaction file is available.

**Important:**  
Please store the extracted file as:

```plaintext
user-wallet-transactions-sample.json

## Files Included

wallet_score_generator.py → End-to-end scoring script
readme.md → Methodology, architecture, and running instructions
analysis.md → Score ranges and behavioral breakdown with distribution visualization
user-wallet-transactions-sample -> small sample of user-transactions
 

</summary>