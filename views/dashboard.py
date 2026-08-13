import streamlit as st

from components.stock_search import render_stock_search
from components.metrics import display_stock_metrics
from components.charts import display_price_chart, display_volume_chart
from services.alpha_vantage import get_daily_data


def show_dashboard():

    # ==========================================
    # Dashboard Header
    # ==========================================

    st.title("📈 Stock Market Visualization")
    st.write("Search for Stocks and Visualize them.")


    # ==========================================
    # Stock Search
    # ==========================================

    ticker = render_stock_search()


    # ==========================================
    # Fetch and Display Stock Data
    # ==========================================

    if ticker:

        ticker = ticker.upper().strip()

        data = get_daily_data(ticker)

        if data is None:
            st.error(
                "Unable to fetch stock data. "
                "Please check the ticker and try again."
            )
            return


        # ==========================================
        # Stock Metrics
        # ==========================================

        display_stock_metrics(
            ticker,
            data
        )


        # ==========================================
        # Price Chart
        # ==========================================

        display_price_chart(
            ticker,
            data
        )


        # ==========================================
        # Volume Chart
        # ==========================================

        display_volume_chart(
            ticker,
            data
        )