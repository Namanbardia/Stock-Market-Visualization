import streamlit as st


# ==========================================
# Display Stock Metrics
# ==========================================

def display_stock_metrics(ticker, data):

    st.subheader(
        f"{ticker} Stock Analysis"
    )


    # ==========================================
    # Get Latest Prices
    # ==========================================

    latest_price = data["Close"].iloc[-1]

    previous_price = data["Close"].iloc[-2]


    # ==========================================
    # Calculate Price Change
    # ==========================================

    price_change = (
        latest_price - previous_price
    )


    percentage_change = (
        price_change / previous_price
    ) * 100


    # ==========================================
    # Display Metric
    # ==========================================

    st.metric(
        label="Current Price",
        value=f"${latest_price:.2f}",
        delta=f"{percentage_change:.2f}%"
    )