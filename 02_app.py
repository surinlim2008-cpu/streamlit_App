import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Global Top10 Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("🌎 Global Top10 Stock Dashboard")
st.caption("최근 1년간 글로벌 시가총액 Top10 기업의 주가를 확인해보세요.")

# 시가총액 Top10 (2025~2026 기준)
stocks = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Meta": "META",
    "Saudi Aramco": "2222.SR",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Berkshire Hathaway": "BRK-B"
}

selected = st.sidebar.selectbox(
    "기업 선택",
    list(stocks.keys())
)

show_volume = st.sidebar.checkbox("거래량 표시", True)
show_ma20 = st.sidebar.checkbox("20일 이동평균", True)
show_ma60 = st.sidebar.checkbox("60일 이동평균", False)

ticker = stocks[selected]

data = yf.download(
    ticker,
    period="1y",
    auto_adjust=True,
    progress=False
)

if data.empty:
    st.error("데이터를 불러오지 못했습니다.")
    st.stop()

# 이동평균
data["MA20"] = data["Close"].rolling(20).mean()
data["MA60"] = data["Close"].rolling(60).mean()

# 현재가
current = float(data["Close"].iloc[-1])
start = float(data["Close"].iloc[0])

change = (current-start)/start*100

high = float(data["High"].max())
low = float(data["Low"].min())

col1,col2,col3,col4 = st.columns(4)

col1.metric("현재가", f"${current:,.2f}")
col2.metric("1년 수익률", f"{change:.2f}%")
col3.metric("최고가", f"${high:,.2f}")
col4.metric("최저가", f"${low:,.2f}")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data.index,
        y=data["Close"],
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

if show_volume:

    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Volume"],
            name="Volume",
            yaxis="y2",
            opacity=0.3
        )
    )

    fig.update_layout(
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title='Volume'
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=700,
    hovermode="x unified",
    title=f"{selected} ({ticker})",
    xaxis_title="Date",
    yaxis_title="Price (USD)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("최근 데이터")

st.dataframe(
    data.tail(20),
    use_container_width=True
)
