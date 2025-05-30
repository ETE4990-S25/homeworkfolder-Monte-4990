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
    folder = os.path.join(data_dir, currency)
    if not os.path.exists(folder):
        logging.warning(f"Missing folder for currency: {currency}")
        return pd.DataFrame()

    files = sorted(os.listdir(folder))
    records = []

    for file in files:
        path = os.path.join(folder, file)
        with open(path, 'r') as f:
            try:
                data = json.load(f)
                items = data.get("channel", {}).get("item", [])
                if isinstance(items, dict):
                    items = [items]  # ensure always list
                for item in items:
                    try:
                        record = {
                            "date": file.replace(".json", ""),
                            "currency": currency,
                            "target": item.get("targetCurrency", ""),
                            # for those commas in the rate
                            "rate": float(item.get("exchangeRate", "0").replace(",", ""))
                        }
                        records.append(record)
                    except Exception as parse_error:
                        logging.error(f"Failed to parse rate in {file} for {currency}: {parse_error}")
            except Exception as file_error:
                logging.error(f"Failed to parse {file} for {currency}: {file_error}")
    return pd.DataFrame(records)



# Load 5 currencies
currencies = ["CHF", "HUF", "INR", "KRW", "SAR"]
dfs = [load_currency_data(cur) for cur in currencies]
dfs = [df for df in dfs if not df.empty]

if not dfs:
    print("No data was loaded. Make sure your folder with json files exists.")
    exit()

df_all = pd.concat(dfs)
print(f" Loaded {len(df_all)} rows from {len(dfs)} currencies.")

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

# Findings:
# CHF the Swiss franc's exchange rate increases the most in 2021-2022
# KRW the South Korean won's exchange rate decreases the most throughout the years
# SAR the saudi riyal is the second most changing currency
# least changing currencies are INR, HUF and KRW
# CHF has highest 30-day rolling volatility and standard deviation
# HUF has the lowest volatility and standard deviation
# The correlation heatmap shows that INR and HUF are the most correlated
# SAR and CHF are the second most correlated
# CHF and HUF are the least correlated
