import os
import json
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure the logs folder exists
os.makedirs("logs", exist_ok=True)

# Setup logging
logging.basicConfig(
    filename='logs/quest.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load JSON files from a given currency folder
def load_currency_data(currency, data_dir="data"):
    files = sorted(os.listdir(os.path.join(data_dir, currency)))
    records = []
    for file in files:
        with open(os.path.join(data_dir, currency, file), 'r') as f:
            data = json.load(f)
            entries = data.get("results", [])
            for entry in entries:
                if isinstance(entry, dict):
                    record = {
                        "date": file.replace(".json", ""),
                        "currency": currency,
                        "target": entry.get("@code", ""),
                        "rate": float(entry.get("rate", 0))
                    }
                    records.append(record)
    return pd.DataFrame(records)

# Load 5 currencies
currencies = ["CHF", "HUF", "INR", "KRW", "SAR"]
df_all = pd.concat([load_currency_data(cur) for cur in currencies])

# Convert to datetime and pivot
df_all["date"] = pd.to_datetime(df_all["date"])
pivot_df = df_all.pivot_table(index="date", columns="currency", values="rate")

# Line plot of exchange rates
plt.figure(figsize=(14,6))
sns.lineplot(data=pivot_df)
plt.title("Exchange Rate Trends Over Time")
plt.ylabel("Exchange Rate")
plt.xlabel("Date")
plt.grid(True)
plt.show()

# Rolling with a window of 30
rolling_std = pivot_df.rolling(window=30).std()
plt.figure(figsize=(14,6))
sns.lineplot(data=rolling_std)
plt.title("30-Day Rolling Volatility")
plt.ylabel("Volatility (std dev)")
plt.xlabel("Date")
plt.grid(True)
plt.show()

# heatmap
plt.figure(figsize=(8,6))
sns.heatmap(pivot_df.corr(), annot=True, cmap="coolwarm")
plt.title("Correlation of Currencies")
plt.show()
