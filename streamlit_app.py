import streamlit as st
import yfinance as yf
import pandas as pd

# 設定網頁標題
st.set_page_config(page_title="美股多股對比工具", layout="wide")

st.title("📊 美股多股對比與百分比試算")

# --- 第一區塊：輸入設定 ---
st.subheader("1. 設定股票與百分比")
col_input1, col_input2 = st.columns([2, 1])

with col_input1:
    # 修改後的標籤文字，且預設值改為空白 ""
    stock_inputs = st.text_input("輸入名稱 (例如: TSLA AMD NVDA，多個代號請用空白隔開)", "").upper()
    # 處理字串轉換成列表
    stock_list = [s.strip() for s in stock_inputs.replace(',', ' ').split() if s.strip()][:3]

with col_input2:
    # 讓使用者自訂計算百分比
    target_pct = st.number_input("設定計算百分比 (%)", value=65.0, step=0.1)

# --- 第二區塊：抓取數據與計算 ---
if stock_list:
    data_rows = []
    
    for symbol in stock_list:
        try:
            ticker = yf.Ticker(symbol)
            # 抓取最近兩天資料以獲取昨收價
            hist = ticker.history(period="2d")
            if not hist.empty:
                last_price = hist['Close'].iloc[-1]
                pct_price = last_price * (target_pct / 100)
                
                # 將結果存入清單
                data_rows.append({
                    "股票代號": symbol,
                    "昨日收盤價 (USD)": round(last_price, 2),
                    f"{target_pct}% 價格 (USD)": round(pct_price, 2),
                    "狀態": "✅ 正常"
                })
            else:
                data_rows.append({"股票代號": symbol, "狀態": "❌ 找不到代號"})
        except Exception:
            data_rows.append({"股票代號": symbol, "狀態": "⚠️ 連線出錯"})

    # 轉換成 Pandas DataFrame
    df = pd.DataFrame(data_rows)

    # --- 第三區塊：顯示結果表格 ---
    st.divider()
    st.subheader(f"2. 對比結果表格 ({target_pct}%)")
    
    # 使用 dataframe 顯示漂亮表格
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- 第四區塊：詳細計算卡片 ---
    st.divider()
    st.subheader("3. 快速預覽")
    cols = st.columns(len(stock_list))
    for i, row in enumerate(data_rows):
        if "昨日收盤價 (USD)" in row:
            with cols[i]:
                st.metric(
                    label=row["股票代號"], 
                    value=f"${row['昨日收盤價 (USD)']}", 
                    delta=f"{target_pct}%: ${row[f'{target_pct}% 價格 (USD)']}",
                    delta_color="normal"
                )

else:
    # 如果還沒輸入名稱時顯示的提示
    st.info("💡 請在上方輸入框輸入股票代號（例如：NVDA AAPL GOOGL）來開始計算。")

st.caption("數據來源：Yahoo Finance。表格會根據您輸入的百分比即時連動計算。")


