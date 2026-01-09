import streamlit as st
import yfinance as yf

# 設定網頁標題
st.set_page_config(page_title="美股百分比自訂計算器", layout="centered")

st.title("📊 美股價格與自訂百分比計算")

# 1. 股票代號輸入
stock_id = st.text_input("1. 輸入股票代號 (例如: AMD, TSLA, MU)", "AMD").upper()

# 2. 獲取昨日收盤價
last_price = 0
try:
    ticker = yf.Ticker(stock_id)
    hist = ticker.history(period="2d")
    if not hist.empty:
        last_price = hist['Close'].iloc[-1]
        st.info(f"2. {stock_id} 昨天收盤價：**${last_price:.2f} USD**")
    else:
        st.warning("找不到此代號，請檢查輸入是否正確。")
except Exception as e:
    st.error(f"數據抓取失敗：{e}")

# 3. 輸入持有股數
shares = st.number_input("3. 輸入持有股數", min_value=0.0, value=1.0, step=1.0)
total_usd = last_price * shares
st.success(f"4. 總價值：**${total_usd:,.2f} USD**")

st.divider()

# --- 自行選擇百分比區塊 ---
st.subheader("🎯 自訂百分比試算 (昨日收盤價 × %)")
st.write("您可以直接點擊下方的數字進行修改：")

# 建立三列並排的輸入框
col1, col2, col3 = st.columns(3)

with col1:
    # 使用 number_input 讓使用者可以自行輸入百分比
    p1 = st.number_input("自訂百分比 1 (%)", value=65.0, step=0.1, key="p1_input")
    res1 = last_price * (p1 / 100)
    st.metric(f"計算結果 ({p1}%)", f"${res1:.2f}")

with col2:
    p2 = st.number_input("自訂百分比 2 (%)", value=75.0, step=0.1, key="p2_input")
    res2 = last_price * (p2 / 100)
    st.metric(f"計算結果 ({p2}%)", f"${res2:.2f}")

with col3:
    p3 = st.number_input("自訂百分比 3 (%)", value=85.0, step=0.1, key="p3_input")
    res3 = last_price * (p3 / 100)
    st.metric(f"計算結果 ({p3}%)", f"${res3:.2f}")

st.markdown("---")
st.caption("提示：您可以點擊輸入框旁邊的 + 或 -，或是直接輸入數字後按 Enter 即可完成計算。")

