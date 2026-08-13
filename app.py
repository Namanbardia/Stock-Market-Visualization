import streamlit as st
from views.dashboard import show_dashboard


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Stock Market Visualization",
    page_icon="📈",
    layout="wide"
)


# ==========================================
# Run Dashboard
# ==========================================

show_dashboard()