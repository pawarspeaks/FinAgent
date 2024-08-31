import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
import time
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = os.getenv('RAPIDAPI_HOST')

# Company name to stock symbol mapping
company_symbol_mapping = {
    "Netflix": "NFLX",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Google": "GOOGL",
    "Facebook": "META",
    "Tesla": "TSLA",
    "Nvidia": "NVDA",
}

# Initialize cache in session state
if 'cache' not in st.session_state:
    st.session_state.cache = {}

def fetch_stock_data(symbol):
    # Check if data is in cache and not expired
    if symbol in st.session_state.cache:
        cached_data, timestamp = st.session_state.cache[symbol]
        if datetime.now() - timestamp < timedelta(minutes=15):  # Cache for 15 minutes
            return cached_data

    base_url = f"https://financebird.p.rapidapi.com/quote/{symbol}/summary"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        # Store in cache
        st.session_state.cache[symbol] = (data, datetime.now())
        return data
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            st.warning("Rate limit exceeded. Using cached data if available.")
            return st.session_state.cache.get(symbol, (None, None))[0]
        else:
            st.error(f"Failed to fetch data. Error: {str(e)}")
            return None

def extract_relevant_data(data):
    if not data or "quoteResponse" not in data or "result" not in data["quoteResponse"] or not data["quoteResponse"]["result"]:
        return None

    result = data["quoteResponse"]["result"][0]
    relevant_data = {}
    fields = [
        "regularMarketPrice", "regularMarketPreviousClose", "regularMarketDayHigh",
        "regularMarketDayLow", "regularMarketVolume", "marketCap", "trailingPE",
        "forwardPE", "dividendYield"
    ]
    
    for field in fields:
        if field in result:
            value = result[field]
            if isinstance(value, dict) and "raw" in value:
                relevant_data[field] = value["raw"]
            else:
                relevant_data[field] = value

    return relevant_data

def calculate_growth_percentage(current, previous):
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def format_large_number(number):
    if number >= 1e12:
        return f"{number / 1e12:.2f}T"
    elif number >= 1e9:
        return f"{number / 1e9:.2f}B"
    elif number >= 1e6:
        return f"{number / 1e6:.2f}M"
    else:
        return f"{number:.2f}"

def show():
    st.title("FinAgent Stock Comparison")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Company 1")
        company1 = st.selectbox("Select Company 1", list(company_symbol_mapping.keys()), key="company1")
        
    with col2:
        st.subheader("Company 2")
        company2 = st.selectbox("Select Company 2", list(company_symbol_mapping.keys()), key="company2")

    if st.button("Compare"):
        if company1 and company2:
            stock_symbol1 = company_symbol_mapping[company1]
            stock_symbol2 = company_symbol_mapping[company2]
            
            with st.spinner("Fetching data..."):
                data1 = fetch_stock_data(stock_symbol1)
                data2 = fetch_stock_data(stock_symbol2)
                
                if data1 and data2:
                    extracted_data1 = extract_relevant_data(data1)
                    extracted_data2 = extract_relevant_data(data2)
                    
                    if extracted_data1 and extracted_data2:
                        comparison_data = {
                            "Metric": [
                                "Current Price", "Previous Close", "Day High", "Day Low",
                                "Volume", "Market Cap", "Trailing P/E", "Forward P/E",
                                "Dividend Yield", "Daily Change %"
                            ],
                            company1: [],
                            company2: []
                        }
                        
                        for company, data in [(company1, extracted_data1), (company2, extracted_data2)]:
                            comparison_data[company].extend([
                                f"${data['regularMarketPrice']:.2f}",
                                f"${data['regularMarketPreviousClose']:.2f}",
                                f"${data['regularMarketDayHigh']:.2f}",
                                f"${data['regularMarketDayLow']:.2f}",
                                format_large_number(data['regularMarketVolume']),
                                format_large_number(data['marketCap']),
                                f"{data['trailingPE']:.2f}",
                                f"{data['forwardPE']:.2f}",
                                f"{data.get('dividendYield', 0):.2f}%",
                                f"{calculate_growth_percentage(data['regularMarketPrice'], data['regularMarketPreviousClose']):.2f}%"
                            ])
                        
                        df_comparison = pd.DataFrame(comparison_data)
                        st.write("### Stock Comparison")
                        st.table(df_comparison.set_index("Metric"))
                        
                        # Highlight key differences
                        st.write("### Key Differences")
                        price_diff = abs(extracted_data1['regularMarketPrice'] - extracted_data2['regularMarketPrice'])
                        volume_diff = abs(extracted_data1['regularMarketVolume'] - extracted_data2['regularMarketVolume'])
                        market_cap_diff = abs(extracted_data1['marketCap'] - extracted_data2['marketCap'])
                        
                        st.write(f"- Price Difference: ${price_diff:.2f}")
                        st.write(f"- Volume Difference: {format_large_number(volume_diff)}")
                        st.write(f"- Market Cap Difference: {format_large_number(market_cap_diff)}")
                        
                    else:
                        st.error("Failed to extract relevant data for comparison.")
                else:
                    st.error("Failed to fetch data for one or both companies. Please try again later.")
        else:
            st.error("Please select both companies.")

if __name__ == "__main__":
    show()