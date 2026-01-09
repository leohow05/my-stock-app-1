import streamlit as st
import yfinance as yf
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="美股多股對比工具", layout="wide")

st.title("📊 美股多股對比：同百分比計算表")

# --- 第一區塊：輸入設定 ---
st.subheader("1. 設定股票與百分比")
col_input, col_p1, col_p2, col_p3 = st.columns([2, 1, 1, 1])

with col_input:
    # 第一欄標題：輸入名稱
    stock_inputs = st.text_input("輸入名稱 (例如: AMD MU TSLA，用空白隔開)", "").upper()
    # 取得前三個代號
    stock_list = [s.strip() for s in stock_inputs.replace(',', ' ').split() if s.strip()][:3]

with col_p1:
    pct1 = st.number_input("百分比 A (%)", value=65.0, step=0.1, key="p1")

with col_p2:
    pct2 = st.number_input("百分比 B (%)", value=75.0, step=0.1, key="p2")

with col_p3:
    pct3 = st.number_input("百分比 C (%)", value=85.0, step=0.1, key="p3")

# --- 第二區塊：抓取數據並計算表格內容 ---
if stock_list:
    data_rows = []
    
    for symbol in stock_list:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            if not hist.empty:
                last_price = hist['Close'].iloc[-1]
                
                # 計算該股票在三個百分比下的數值
                val1 = last_price * (pct1 / 100)
                val2 = last_price * (pct2 / 100)
                val3 = last_price * (pct3 / 100)
                
                # 建立表格的一列資料
                data_rows.append({
                    "股票代號": symbol,
                    "昨日收盤價": f"{last_price:.2f}",
                    f"方案 A ({pct1}%)": f"{val1:.2f}",
                    f"方案 B ({pct2}%)": f"{val2:.2f}",
                    f"方案 C ({pct3}%)": f"{val3:.2f}"
                })
            else:
                data_rows.append({"股票代號": symbol, "昨日收盤價": "找無資料", f"方案 A ({pct1}%)": "-", f"方案 B ({pct2}%)": "-", f"方案 C ({pct3}%)": "-"})
        except Exception:
            data_rows.append({"股票代號": symbol, "昨日收盤價": "連線錯誤", f"方案 A ({pct1}%)": "-", f"方案 B ({pct2}%)": "-", f"方案 C ({pct3}%)": "-"})

    # 轉換成 Pandas DataFrame
    df = pd.DataFrame(data_rows)

    # --- 第三區塊：顯示表格 ---
    st.divider()
    st.subheader("2. 多股對比數據表")
    
    # 使用 dataframe 顯示，並自動填滿寬度
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- 第四區塊：視覺化區塊 ---
    st.divider()
    st.subheader("3. 同百分比橫向對照")
    
    # 依百分比分類顯示，方便直接比較三支股票
    tab1, tab2, tab3 = st.tabs([f"對比 {pct1}%", f"對比 {pct2}%", f"對比 {pct3}%"])
    
    with tab1:
        cols = st.columns(len(data_rows))
        for i, row in enumerate(data_rows):
            if row[f"方案 A ({pct1}%)"] != "-":
                cols[i].metric(row["股票代號"], f"${row[f'方案 A ({pct1}%)']}", f"原價: ${row['昨日收盤價']}")

    with tab2:
        cols = st.columns(len(data_rows))
        for i, row in enumerate(data_rows):
            if row[f"方案 B ({pct2}%)"] != "-":
                cols[i].metric(row["股票代號"], f"${row[f'方案 B ({pct2}%)']}", f"原價: ${row['昨日收盤價']}")

    with tab3:
        cols = st.columns(len(data_rows))
        for i, row in enumerate(data_rows):
            if row[f"方案 C ({pct3}%)"] != "-":
                cols[i].metric(row["股票代號"], f"${row[f'方案 C ({pct3}%)']}", f"原價: ${row['昨日收盤價']}")

else:
    st.info("💡 請在上方輸入框輸入股票代號（例如：AMD MU TSLA）來開始計算。")

st.caption("數據來源：Yahoo Finance。此工具會自動抓取最近一個交易日的收盤價進行百分比換算。")



