import requests
import json
from datetime import datetime

# Function to fetch stock data from the Alpha Vantage API
def fetch_stock_data(symbol, function, api_key):
    # Alpha Vantage API URL
    url = f"https://www.alphavantage.co/query"
    
    # Define parameters for the API request
    params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "compact",  # For larger datasets, change this to "full"
    }
    
    # Make the request
    print(f"Fetching data for {symbol} from {function}...")
    response = requests.get(url, params=params)
    
    # Check for a successful response
    if response.status_code == 200:
        print("Data fetched successfully!")
        data = response.json()
        print(f"Response from API: {data}")  # Print the entire response for debugging
        return data
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Function to parse the stock data received from the API
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

# Function to filter stock data by a given date range
def filter_by_date_range(parsed_data, start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    filtered_data = [entry for entry in parsed_data if start <= datetime.strptime(entry["date"], "%Y-%m-%d") <= end]
    return filtered_data

# Main function to get stock data, parse it, and filter by date range
def get_stock_data(symbol, start_date, end_date, function, api_key):
    # Fetch the data
    data = fetch_stock_data(symbol, function, api_key)
    
    if data:
        # Parse the data
        parsed_data = parse_stock_data(data)
        
        if parsed_data:
            # Filter by date range
            filtered_data = filter_by_date_range(parsed_data, start_date, end_date)
            return filtered_data
        else:
            print("Error parsing data.")
            return None
    else:
        print("Error fetching data.")
        return None

# Test the function
if __name__ == "__main__":
    api_key = "1M1XTV42PNTYEAEU"
    symbol = "IBM"
    start_date = "2023-01-01"
    end_date = "2023-10-15"
    function = "TIME_SERIES_DAILY"

    stock_data = get_stock_data(symbol, start_date, end_date, function, api_key)

    if stock_data:
        for entry in stock_data:
            print(entry)
