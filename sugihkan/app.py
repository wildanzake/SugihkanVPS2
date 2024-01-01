from datetime import datetime, timedelta
import os
import time
import pandas as pd
import yfinance as yf

def update_crypto_data(crypto_pair):
    file_path = f"{crypto_pair.lower()}_data.csv"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)  # Set start_date to 7 days ago

    if os.path.exists(file_path):
        existing_data = pd.read_csv(file_path)
        if not existing_data.empty:
            last_date_str = existing_data['Datetime'].max()
            last_date = pd.to_datetime(last_date_str)
            last_date = last_date.replace(tzinfo=None)  # Make last_date offset-naive
            # Only update start_date if it's older than last_date in file
            if last_date > start_date:
                start_date = last_date + timedelta(minutes=1)
    else:
        existing_data = pd.DataFrame()

    # Check if start date is before the current time
    if start_date < end_date:
        new_data = yf.download(crypto_pair, start=start_date, end=end_date, interval='1m')
        if not new_data.empty:
            new_data.reset_index(inplace=True)
            new_data.rename(columns={'index': 'Datetime'}, inplace=True)
            updated_data = pd.concat([existing_data, new_data])
            updated_data.to_csv(file_path, index=False)

    return file_path

cryptos = ["BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD"]

while True:
    for crypto in cryptos:
        update_crypto_data(crypto)
    time.sleep(60)  # Wait for one minute before next update
