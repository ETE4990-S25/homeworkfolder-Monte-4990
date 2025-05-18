import os
import requests
import xmltodict
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import random
import logging

logging.basicConfig(filename='logs/quest.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "https://www.floatrates.com/historical-exchange-rates.html"
OUTPUT_DIR = "data"
MAX_THREADS = 10
RATES = ["EUR", "GBP", "USD", "DZD", "AUD", "BWP", "BND", "CAD", "CLP", "CNY", "COP", "CZK",
         "DKK", "HUF", "ISK", "INR", "IDR", "ILS", "KZT", "KRW", "KWD", "LYD", "MYR", "MUR",
         "NPR", "NZD", "NOK", "OMR", "PKR", "PLN", "QAR", "RUB", "SAR", "SGD", "ZAR", "LKR",
         "SEK", "CHF", "THB", "TTD"]
BASES = [r for r in RATES if r not in ["USD", "EUR", "GBP"]]

def parse_xml_to_json(xml_text: str) -> dict:
    """
    Converts XML text to a python dictionary
    """
    try:
        return xmltodict.parse(xml_text)
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}")

def save_json(data: dict, filepath: str):
    """
    Save dictionary to json file
    """
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    with open("sample.xml", "r") as f:
        xml_data = f.read()
    parsed = parse_xml_to_json(xml_data)
    save_json(parsed, "cleaned_sample.json")
