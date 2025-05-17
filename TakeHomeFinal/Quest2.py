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

