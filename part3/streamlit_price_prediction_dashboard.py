import pandas as pd
import plotly.express as px
import streamlit as st

from main import PREDICTION_FILE_PATH


@st.cache_data
def load_data():
    df = pd.read_csv(PREDICTION_FILE_PATH)
    df["date"] = pd.to_datetime(df["date"])
    return df


df = load_data()
df.rename(columns={"next_day_close": "actual_price"}, inplace=True)

tickers = df["name"].unique()
selected_ticker = st.sidebar.selectbox("Select a Stock Ticker", tickers)

filtered_df = df[df["name"] == selected_ticker]

fig = px.line(filtered_df, x="date", y=["actual_price", "predicted_price"],
              labels={"value": "Closing Price", "date": "Date"},
              title=f"Actual vs. Predicted Closing Prices for {selected_ticker}",
              color_discrete_map={"actual_price": "blue", "predicted_price": "red"})

st.plotly_chart(fig)
