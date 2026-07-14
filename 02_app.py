import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌍 Global Market Cap Top 10 Dashboard")
st.markdown("최근 1년 동안 글로벌 시가총액 Top10 기업의 주가를 확인할 수 있습니다.")

stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Berkshire Hathaway": "BRK-B",
    "Saudi Aramco": "2222.SR"
}

company = st.sidebar.selectbox(
    "기업 선택",
    list(stocks.keys())
)

ticker = stocks[company]

period = st.sidebar.selectbox(
    "기간",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=3
)

show_ma20 = st.sidebar.checkbox("20일 이동평균", True)
show_ma60 = st.sidebar.checkbox("60일 이동평균", False)

with st.spinner("데이터 불러오는 중..."):

    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

# yfinance 최신버전 대응
if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.droplevel(1)

if data.empty:
    st.error("주가 데이터를 가져오지 못했습니다.")
    st.stop()

close = data["Close"]
high = data["High"]
low = data["Low"]

data["MA20"] = close.rolling(20).mean()
data["MA60"] = close.rolling(60).mean()

current = close.iloc[-1]
start = close.iloc[0]

change = (current-start)/start*100

col1,col2,col3,col4 = st.columns(4)

col1.metric("현재가", f"${current:.2f}")
col2.metric("수익률", f"{change:.2f}%")
col3.metric("최고가", f"${high.max():.2f}")
col4.metric("최저가", f"${low.min():.2f}")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=close,
        mode="lines",
        name="Close",
        line=dict(width=3)
    )
)

if show_ma20:
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA20"],
            name="MA20"
        )
    )

if show_ma60:
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["MA60"],
            name="MA60"
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=650,
    hovermode="x unified",
    title=f"{company} ({ticker})",
    xaxis_title="Date",
    yaxis_title="Price"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("최근 데이터")

st.dataframe(
    data.tail(20),
    use_container_width=True
)
