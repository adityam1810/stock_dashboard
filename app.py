import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

# ----------- CONFIG --------------
API_KEY = 'DIIW2PEAP0I9IHJI'  # <-- Replace this with your API key
st.set_page_config(layout="wide")
st.title("📈 Real-Time Stock Market Dashboard")

# ----------- SIDEBAR --------------
symbol = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, TSLA)", value="AAPL")
interval = st.sidebar.selectbox("Select Time Interval", ["1min", "5min", "15min", "30min", "60min"])

# ----------- FETCH DATA --------------
def get_stock_data(symbol, interval):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()

    key = [k for k in data.keys() if "Time Series" in k]
    if not key:
        return None

    df = pd.DataFrame.from_dict(data[key[0]], orient='index')
    df = df.astype(float)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df

df = get_stock_data(symbol, interval)

# ----------- DISPLAY DATA --------------
if df is not None:
    st.subheader(f"📊 Stock Price for {symbol}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['1. open'], name='Open', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['4. close'], name='Close', line=dict(color='green')))
    fig.update_layout(xaxis_title='Time', yaxis_title='Price (USD)', template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 Latest Data")
    st.dataframe(df.tail())
else:
    st.warning("⚠️ Failed to fetch data. Please check symbol or API limit.")
