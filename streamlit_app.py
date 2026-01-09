import streamlit as st
import yfinance as yf
import requests

# 設定網頁標題
st.set_page_config(page_title="美股資產計算器", layout="centered")

st.title("📈 美股資產換算工具")

# 1. 股票名稱輸入 (第一格)
stock_id = st.text_input("輸入股票代號 (如: AMD, TSLA, MU)", "AMD").upper()

# 2. 獲取昨日收盤價 (第二格)
try:
    ticker = yf.Ticker(stock_id)
    # 取最近兩天的資料獲取昨收價
    hist = ticker.history(period="2d")
    if not hist.empty:
        last_price = hist['Close'].iloc[-1]
        st.info(f"{stock_id} 昨天收盤價：**${last_price:.2f} USD**")
    else:
        st.warning("找不到該代號，請檢查輸入是否正確。")
        last_price = 0
except Exception as e:
    st.error(f"數據抓取失敗：{e}")
    last_price = 0

# 3. 輸入股數 (第三格)
shares = st.number_input("輸入持有股數", min_value=0.0, value=1.0, step=1.0)

# 4. 總價格計算 (第四格)
total_usd = last_price * shares
st.success(f"總價值：**${total_usd:,.2f} USD**")

st.divider()

# 額外功能：匯率換算
st.subheader("多國匯率換算")
try:
    # 獲取即時匯率
    res = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rates = res.json().get("rates", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("台幣 (TWD)", f"{total_usd * rates.get('TWD', 32.5):,.0f}")
    with col2:
        st.metric("人民幣 (CNY)", f"{total_usd * rates.get('CNY', 7.2):,.2f}")
    with col3:
        st.metric("日圓 (JPY)", f"{total_usd * rates.get('JPY', 150):,.0f}")
except:
    st.write("目前無法取得即時匯率數據。")

st.caption("數據來源：Yahoo Finance & ExchangeRate-API")
