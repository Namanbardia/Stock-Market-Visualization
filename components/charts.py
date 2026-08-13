import streamlit as st
import plotly.graph_objects as go


# ==========================================
# Display Price Chart
# ==========================================

def display_price_chart(ticker, data):

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
# Display Volume Chart
# ==========================================

def display_volume_chart(ticker, data):

    st.subheader("📊 Trading Volume")

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume"
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume",
        height=400,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )