import requests
import streamlit as st
import pandas as pd


# ==========================================
# Alpha Vantage Configuration
# ==========================================

API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]

BASE_URL = "https://www.alphavantage.co/query"


# ==========================================
# Get Daily Stock Data
# ==========================================

def get_daily_data(ticker):

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "outputsize": "compact",
        "apikey": API_KEY
    }

    try:

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

    except requests.exceptions.RequestException as e:

        st.error(f"Network error: {e}")
        return None


    # ==========================================
    # Handle API Errors
    # ==========================================

    if "Error Message" in result:

        st.error(
            "Invalid stock ticker. "
            "Please enter a valid symbol."
        )

        return None


    if "Note" in result:

        st.warning(
            "Alpha Vantage API request limit reached. "
            "Please try again later."
        )

        return None


    if "Information" in result:

        st.warning(result["Information"])

        return None


    # ==========================================
    # Extract Time Series
    # ==========================================

    time_series = result.get("Time Series (Daily)")


    if not time_series:

        st.error(
            "No stock data found for this ticker."
        )

        return None


    # ==========================================
    # Convert JSON → DataFrame
    # ==========================================

    data = pd.DataFrame.from_dict(
        time_series,
        orient="index"
    )


    # ==========================================
    # Rename Columns
    # ==========================================

    data = data.rename(
        columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }
    )


    # ==========================================
    # Convert Values to Numeric
    # ==========================================

    for column in [
        "Open",
        "High",
        "Low",
        "Close",
        "Volume"
    ]:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )


    # ==========================================
    # Convert Index to Date
    # ==========================================

    data.index = pd.to_datetime(data.index)

    data = data.sort_index()


    return data