import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Stock Market Visualization",
    page_icon="📈",
    layout="wide"
)


# ==========================================
# Alpha Vantage Configuration
# ==========================================

API_KEY = st.secrets["ALPHA_VANTAGE_API_KEY"]

BASE_URL = "https://www.alphavantage.co/query"


# ==========================================
# App Title
# ==========================================

st.title("📈 Stock Market Visualization")
st.write("Search for Stocks and Visualize them.")


# ==========================================
# Ticker Search
# ==========================================

if "ticker" not in st.session_state:
    st.session_state.ticker = ""


def select_stock(symbol):
    st.session_state.ticker = symbol


ticker = st.text_input(
    "Enter Stock Symbol/Ticker",
    placeholder="Example: AAPL, MSFT, RELIANCE...",
    key="ticker"
)


# ==========================================
# Popular Stocks
# ==========================================

st.write("Popular Stocks")

col1, col2, col3, col4, col5, col6 = st.columns(6)

stocks = [
    "AAPL",
    "MSFT",
    "GOOGL",
    "AMZN",
    "TSLA",
    "NVDA"
]

for col, symbol in zip(
    [col1, col2, col3, col4, col5, col6],
    stocks
):
    with col:
        st.button(
            symbol,
            use_container_width=True,
            on_click=select_stock,
            args=(symbol,)
        )


# ==========================================
# Fetch Stock Data
# ==========================================

if ticker:

    ticker = ticker.upper().strip()

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
        st.stop()


    # ==========================================
    # Handle API Errors
    # ==========================================

    if "Error Message" in result:

        st.error(
            "Invalid stock ticker. Please enter a valid symbol."
        )
        st.stop()


    if "Note" in result:

        st.warning(
            "Alpha Vantage API request limit reached. "
            "Please try again later."
        )
        st.stop()


    if "Information" in result:

        st.warning(result["Information"])
        st.stop()


    # ==========================================
    # Extract Time Series
    # ==========================================

    time_series = result.get("Time Series (Daily)")


    if not time_series:

        st.error(
            "No stock data found for this ticker."
        )
        st.stop()


    # ==========================================
    # Convert JSON → DataFrame
    # ==========================================

    data = pd.DataFrame.from_dict(
        time_series,
        orient="index"
    )


    # Rename Columns

    data = data.rename(
        columns={
            "1. open": "Open",
            "2. high": "High",
            "3. low": "Low",
            "4. close": "Close",
            "5. volume": "Volume"
        }
    )


    # Convert values to numeric

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


    # Convert index to Date

    data.index = pd.to_datetime(data.index)

    data = data.sort_index()


    # ==========================================
    # Stock Header
    # ==========================================

    st.subheader(
        f"{ticker} Stock Analysis"
    )


    # ==========================================
    # Current Price
    # ==========================================

    latest_price = data["Close"].iloc[-1]

    previous_price = data["Close"].iloc[-2]


    price_change = (
        latest_price - previous_price
    )


    percentage_change = (
        price_change / previous_price
    ) * 100


    st.metric(
        label="Current Price",
        value=f"${latest_price:.2f}",
        delta=f"{percentage_change:.2f}%"
    )


    # ==========================================
    # Price Chart
    # ==========================================

    st.subheader("📈 Price Chart")


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price"
        )
    )


    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        height=500,
        hovermode="x unified"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ==========================================
    # Volume Chart
    # ==========================================

    st.subheader("📊 Trading Volume")


    volume_fig = go.Figure()


    volume_fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume"
        )
    )


    volume_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        height=400,
        hovermode="x unified"
    )


    st.plotly_chart(
        volume_fig,
        use_container_width=True
    )