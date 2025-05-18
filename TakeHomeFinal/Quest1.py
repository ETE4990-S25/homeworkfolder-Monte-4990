import os
import requests
import xmltodict
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import random
import logging

# Make sure the logs directory exists
os.makedirs("logs", exist_ok=True)

# Set up logging file
logging.basicConfig(
    filename='logs/quest.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# logging setup

logging.basicConfig(filename='logs/quest.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Them constants / Money names

BASE_URL = "https://www.floatrates.com/historical-exchange-rates.html"
OUTPUT_DIR = "data"
MAX_THREADS = 10
RATES = ["EUR", "GBP", "USD", "DZD", "AUD", "BWP", "BND", "CAD", "CLP", "CNY", "COP", "CZK",
         "DKK", "HUF", "ISK", "INR", "IDR", "ILS", "KZT", "KRW", "KWD", "LYD", "MYR", "MUR",
         "NPR", "NZD", "NOK", "OMR", "PKR", "PLN", "QAR", "RUB", "SAR", "SGD", "ZAR", "LKR",
         "SEK", "CHF", "THB", "TTD"]
BASES = [r for r in RATES if r not in ["USD", "EUR", "GBP"]]

# Generate thy range between two dates

def generate_date_range(start: str, end: str) -> list:
    s = datetime.strptime(start, "%Y-%m-%d")
    e = datetime.strptime(end, "%Y-%m-%d")
    return [(s + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((e - s).days + 1)]


# Download thy data for a single date
def download_single_date(date: str, base: str):
    folder = os.path.join(OUTPUT_DIR, base)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f"{date}.json")

    # Check if the file already exists
    if os.path.exists(filename):
        logging.warning(f"{filename} already exists. Skipping file.")
        return
    

    # Check if the file is older than 1 day
    url = f"{BASE_URL}?operation=rates&pb_id=1775&page=historical&currency_date={date}&base_currency_code={base}&format_type=xml"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data_dict = xmltodict.parse(response.text)
        with open(filename, "w") as f:
            json.dump(data_dict, f, indent=2)
        logging.info(f"Downloaded {base} for {date}")
    except Exception as e:
        logging.error(f"Failed for {base} on {date}: {e}")

# Download thy data for all dates from may the fourth be with you to the end
def download_all(base: str, start_date="2011-05-04", end_date=None):
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")
    dates = generate_date_range(start_date, end_date)
    logging.info(f"Starting downloads for {base} from {start_date} to {end_date}")
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for date in dates:
            executor.submit(download_single_date, date, base)


if __name__ == "__main__":
    currencies = ["CHF", "HUF", "INR", "KRW", "SAR"]
    for currency in currencies:
        download_all(currency, start_date="2011-05-04")