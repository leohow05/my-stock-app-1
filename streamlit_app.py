import streamlit as st
import yfinance as yf
import requests

# 網頁基礎設定
st.set_page_config(page_title="美股資產計算器", layout="centered")

st.title("📈 美股資產換算工具")

# 第一格：股票代號輸入
stock_id = st.text_input("第一格：輸入股票代號 (如: AMD, TSLA, MU)", "AMD").upper()

# 第二格：獲取昨日收盤價
try:
    ticker = yf.Ticker(stock_id)
    # 取最近兩天的資料
    hist = ticker.history(period="2d")
    if not hist.empty:
        last_price = hist['Close'].iloc[-1]
        st.info(f"第二格：{stock_id} 昨天收盤價為 **${last_price:.2f} USD**")
    else:
        st.error("找不到該股票代號，請重新輸入。")
        last_price = 0
except Exception as e:
    st.error(f"連線失敗: {e}")
    last_price = 0

# 第三格：股數輸入
shares = st.number_input("第三格：輸入持有股數", min_value=0.0, value=1.0, step=1.0)

# 第四格：總價格計算
total_usd = last_price * shares
st.success(f"第四格：總價值約為 **${total_usd:,.2f} USD**")

st.divider()

# 額外功能：匯率換算
st.subheader("多國匯率換算")
try:
    # 獲取即時匯率 API
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rates = response.json().get("rates", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("台幣 (TWD)", f"{total_usd * rates.get('TWD', 32.5):,.0f}")
    with col2:
        st.metric("人民幣 (CNY)", f"{total_usd * rates.get('CNY', 7.2):,.2f}")
    with col3:
        st.metric("日圓 (JPY)", f"{total_usd * rates.get('JPY', 150):,.0f}")
except:
    st.write("暫時無法取得最新匯率，請稍後再試。")

st.caption("數據來源: Yahoo Finance & ExchangeRate API")