import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
API_KEY = os.getenv('RAPIDAPI_KEY')
API_HOST = os.getenv('RAPIDAPI_HOST')

def get_stock_recommendation(stock, user_profile):
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': API_HOST
    }
    
    # Fetch company overview
    url_overview = f"https://{API_HOST}/query?function=OVERVIEW&symbol={stock}&datatype=json"
    response_overview = requests.get(url_overview, headers=headers)
    data_overview = response_overview.json()
    
    # Fetch time series data
    url_time_series = f"https://{API_HOST}/query?function=QUOTE_ENDPOINT&symbol={stock}&datatype=json"
    response_time_series = requests.get(url_time_series, headers=headers)
    data_time_series = response_time_series.json()
    
    pe_ratio = float(data_overview.get('PERatioTTM', 0))
    dividend_yield = float(data_overview.get('DividendYield', 0))
    beta = float(data_overview.get('Beta', 0))
    
    # User profile factors
    risk_tolerance = user_profile['investment_mindset'] / 10  # Assuming 1-10 scale
    investment_horizon = user_profile['investment_experience']
    
    # Simple recommendation logic
    score = 0
    if pe_ratio < 15:
        score += 1
    if dividend_yield > 0.02:
        score += 1
    if (beta < 1 and risk_tolerance < 0.5) or (beta > 1 and risk_tolerance > 0.5):
        score += 1
    if investment_horizon > 5:
        score += 1
    
    recommendation = "Hold"
    if score >= 3:
        recommendation = "Buy"
    elif score <= 1:
        recommendation = "Sell"
    
    return recommendation, {
        "P/E Ratio": pe_ratio,
        "Dividend Yield": f"{dividend_yield:.2%}",
        "Beta": beta,
        "Your Risk Tolerance": f"{risk_tolerance:.1f}/1",
        "Your Investment Horizon": f"{investment_horizon} years"
    }

def compare_stocks_for_user(stock1, stock2, user_profile):
    rec1, metrics1 = get_stock_recommendation(stock1, user_profile)
    rec2, metrics2 = get_stock_recommendation(stock2, user_profile)
    
    comparison = pd.DataFrame({
        'Metric': list(metrics1.keys()) + ['Recommendation'],
        stock1: list(metrics1.values()) + [rec1],
        stock2: list(metrics2.values()) + [rec2]
    })
    
    return comparison
