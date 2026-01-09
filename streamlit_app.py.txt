import tkinter as tk
from tkinter import messagebox, ttk
import yfinance as yf
import requests

def get_data():
    ticker_name = entry_stock.get().upper()
    try:
        # 1. 抓取股價 (取最後一個交易日的收盤價)
        stock = yf.Ticker(ticker_name)
        df = stock.history(period="2d")
        if df.empty:
            messagebox.showerror("錯誤", "找不到該股票代碼")
            return
        
        price = df['Close'].iloc[-1]
        label_price_val.config(text=f"${price:.2f}")
        
        # 2. 計算總價
        shares = float(entry_shares.get() or 0)
        total_usd = price * shares
        label_total_val.config(text=f"${total_usd:,.2f} USD")
        
        # 3. 匯率換算 (抓取即時匯率)
        rate_res = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        rates = rate_res.get("rates", {})
        
        twd = total_usd * rates.get("TWD", 32.5)
        cny = total_usd * rates.get("CNY", 7.2)
        jpy = total_usd * rates.get("JPY", 150.0)
        
        label_rates.config(text=f"台幣 (TWD): {twd:,.0f} 元\n人民幣 (CNY): {cny:,.2f} 元\n日圓 (JPY): {jpy:,.0f} ￥")
        
    except Exception as e:
        messagebox.showerror("錯誤", f"發生問題: {str(e)}")

# 建立視窗介面
root = tk.Tk()
root.title("美股資產計算器")
root.geometry("400x500")
root.padx = 20

# 介面排版
ttk.Label(root, text="第一格：輸入股票代號 (如 AMD, TSLA)").pack(pady=10)
entry_stock = ttk.Entry(root, font=("Arial", 12))
entry_stock.pack()

ttk.Label(root, text="第二格：昨收盤價格").pack(pady=10)
label_price_val = ttk.Label(root, text="---", font=("Arial", 14, "bold"), foreground="blue")
label_price_val.pack()

ttk.Label(root, text="第三格：輸入持有股數").pack(pady=10)
entry_shares = ttk.Entry(root, font=("Arial", 12))
entry_shares.insert(0, "1")
entry_shares.pack()

btn_calc = ttk.Button(root, text="執行計算 (含匯率轉換)", command=get_data)
btn_calc.pack(pady=20)

ttk.Label(root, text="第四格：美金總價格").pack(pady=5)
label_total_val = ttk.Label(root, text="---", font=("Arial", 14, "bold"), foreground="green")
label_total_val.pack()

ttk.Label(root, text="多國匯率換算結果:").pack(pady=15)
label_rates = ttk.Label(root, text="", justify="left", font=("Microsoft JhengHei", 10))
label_rates.pack()

root.mainloop()