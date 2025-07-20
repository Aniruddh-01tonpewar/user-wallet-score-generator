
import json
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle

# loading JSON file 
with open("user-wallet-transactions-sample.json", "r") as f:
    raw_data = json.load(f)

# normalize JSON to extract nested fields
df = pd.json_normalize(raw_data)

# extracting the relevent fields
df = df[["userWallet", "actionData.type", "actionData.amount"]]
df.columns = ["wallet", "action_type", "amount"]
df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
df["amount_log"] = np.log1p(df["amount"]).round(2)

# action score mapping, it helps to quantify the impact of each action type
action_score_map = {
    "Borrow": 2,
    "Repay": 3,
    "Deposit": 5,
    "RedeemUnderlying": 4,
    "LiquidationCall": 1
}
df["action_score"] = df["action_type"].map(action_score_map)

# label the target
target_map = {
    "Borrow": 0,
    "Repay": 0,
    "Deposit": 1,
    "RedeemUnderlying": 1,
    "LiquidationCall": 0
}
df["target"] = df["action_type"].map(target_map)

# training the model using logistic regression
X = df[["amount_log", "action_score"]]
y = df["target"]
X, y = shuffle(X, y, random_state=42)

model = LogisticRegression(class_weight="balanced", solver="liblinear")
model.fit(X, y)

# predicting responsibility score per transaction
df["responsible_prob"] = model.predict_proba(X)[:, 1]

# average probability per wallet
wallet_scores = df.groupby("wallet")["responsible_prob"].mean()
wallet_scores_scaled = (wallet_scores * 1000).round().astype(int)

# output dictionary
user_proba_avg_int = wallet_scores_scaled.to_dict()

# saving as JSON
with open("wallet_scores.json", "w") as out_file:
    json.dump(user_proba_avg_int, out_file, indent=2)

print("Wallet scores generated and saved to wallet_scores.json.")
