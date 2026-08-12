import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Page Configuration 
st.set_page_config(
    page_title = "Stock Market Visualization",
    page_icon = "📈",
    layout = "wide"
)

# App title
# st.title("Stock Market Visualization")
# st.write("Search for Stocks and Visualize them.")

# Ticker Search
# Ticker means short symbol of the company. Example: AAPL is the short symbol/Ticker of Apple company. 

if "ticker" not in st.session_state:
    st.session_state.ticker = ""

def select_stock(symbol):
    st.session_state.ticker = symbol


ticker = st.text_input(
    "Enter Stock Symbol/Ticker",
    placeholder="Example: AAPL, MSFT, TSLA.",
    key="ticker"
)


# Popular Stocks
# st.write("Popular Stocks")

col1, col2, col3, col4, col5, col6 = st.columns(6)

stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]

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

# Fetch Data
if ticker:
    ticker = ticker.upper()

    # Creating the Stock object of the ticker. 
    stock = yf.Ticker(ticker)

    # Creating the info dictonary of the stock
    try:
        info = stock.info

    except yf.exceptions.YFRateLimitError:
        st.error("Yahoo Finance rate limit ho gayi. Thodi der baad try karo.")
        st.stop()
    
    except Exception as e:
        st.error(f"Error: {e}")
        st.stop()

    if not info:
        st.error("Ticker not found. Enter a valid Ticker.")
        st.stop()

    st.subheader(f"{info.get('longName', ticker)} ({ticker})" )
    current_price = info.get("currentPrice")

    if current_price:
        st.metric(
            label = "Current Price",
            value = f"${current_price:.2f}"
        )

    # Historical Data
    data = stock.history(period = "1y")
    if data.empty:
        st.error("No Historical data available.")
        st.stop()

    st.subheader("📊 Price Chart") 

    fig = go.Figure() # Creates empty graph/chart container

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
        height=500
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
