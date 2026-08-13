import streamlit as st


# ==========================================
# Popular Stocks
# ==========================================

POPULAR_STOCKS = [
    "AAPL",
    "GOOGL",
    "NVDA",
    "RELIANCE.BSE",
    "TCS.BSE",
    "HDFCBANK.BSE"
]


# ==========================================
# Select Stock
# ==========================================

def select_stock(symbol):
    st.session_state.ticker = symbol


# ==========================================
# Render Stock Search
# ==========================================

def render_stock_search():

    # Initialize ticker state
    if "ticker" not in st.session_state:
        st.session_state.ticker = ""


    # ------------------------------------------
    # Search Input
    # ------------------------------------------

    ticker = st.text_input(
        "Enter Stock Symbol/Ticker",
        placeholder="Example: AAPL, MSFT, TSLA.",
        key="ticker"
    )


    # ------------------------------------------
    # Popular Stocks
    # ------------------------------------------

    st.write("Popular Stocks")
    st.write("Pro Tip: Use .BSE for Bombay Stock Exchange (BSE) Stocks")

    columns = st.columns(len(POPULAR_STOCKS))


    for column, symbol in zip(
        columns,
        POPULAR_STOCKS
    ):

        with column:

            st.button(
                symbol,
                use_container_width=True,
                on_click=select_stock,
                args=(symbol,)
            )


    return ticker