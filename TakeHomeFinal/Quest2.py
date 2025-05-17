import os
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
currencies = ["EUR", "USD", "GBP", "JPY", "CNY"]
df_all = pd.concat([load_currency_data(cur) for cur in currencies])

# Convert to datetime and pivot
df_all["date"] = pd.to_datetime(df_all["date"])
pivot_df = df_all.pivot_table(index="date", columns="currency", values="rate")

# Line plot of exchange rates
plt.figure(figsize=(14, 6))
sns.lineplot(data=pivot_df)
plt.title("Exchange Rate Trends Over Time")
plt.ylabel("Exchange Rate (vs Base)")
plt.grid()
plt.show()

# Rolling with a window of 30
rolling_vol = pivot_df.rolling(window=30).std()
plt.figure(figsize=(14, 6))
sns.lineplot(data=rolling_vol)
plt.title("30-Day Rolling Volatility")
plt.ylabel("Volatility")
plt.grid()
plt.show()

# heatmap
corr = pivot_df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Currency Correlation Heatmap")
plt.show()
