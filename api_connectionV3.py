import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt

def fetch_stock_data(symbol, function, api_key):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full",  # For smaller datasets (last 100 days) change this to "compact"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Data fetched successfully!")
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def parse_stock_data(data):
    if "Time Series (Daily)" in data:
        daily_data = data["Time Series (Daily)"]
        parsed_data = []
        for date, values in daily_data.items():
            parsed_data.append({
                "date": date,
                "open": float(values["1. open"]),
                "high": float(values["2. high"]),
                "low": float(values["3. low"]),
                "close": float(values["4. close"]),
                "volume": int(values["5. volume"])
            })
        return parsed_data
    else:
        print("No daily data found in response.")
        return None

def filter_by_date_range(parsed_data, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    today = datetime.today()
    end = min(end, today)  
    
    filtered_data = [entry for entry in parsed_data if start <= datetime.strptime(entry["date"], "%Y-%m-%d") <= end]
    return filtered_data

def generate_chart(filtered_data, stock_symbol, chart_type):
    dates = [entry["date"] for entry in filtered_data]
    closing_prices = [entry["close"] for entry in filtered_data]

    plt.figure(figsize=(10,5))
    
    if chart_type == "line":
        plt.plot(dates, closing_prices, label='Close Price', marker='o')
    elif chart_type == "bar":
        plt.bar(dates, closing_prices, label='Close Price')
    
    plt.title(f"{stock_symbol} Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

def get_valid_date_range():
    while True:
        start_date = input("Enter the start date (YYYY-MM-DD): ")
        end_date = input("Enter the end date (YYYY-MM-DD): ")

        if end_date >= start_date:
            return start_date, end_date
        else:
            print("Invalid date range. End date cannot be before start date. Please enter the dates again.")

def main():
    api_key = "1M1XTV42PNTYEAEU"
    symbol = input("Enter the stock symbol (e.g., IBM): ").upper()

    start_date, end_date = get_valid_date_range()

    today = datetime.today().strftime('%Y-%m-%d')
    if end_date > today:
        print(f"End date can't be after today's date: {today}. Adjusting to {today}.")
        end_date = today

    chart_type = input("Enter chart type (line/bar): ").lower()
    function = "TIME_SERIES_DAILY"

    stock_data = fetch_stock_data(symbol, function, api_key)

    if stock_data:
        parsed_data = parse_stock_data(stock_data)
        filtered_data = filter_by_date_range(parsed_data, start_date, end_date)

        if filtered_data:
            generate_chart(filtered_data, symbol, chart_type)
        else:
            print("No data found for the specified date range.")

if __name__ == "__main__":
    main()