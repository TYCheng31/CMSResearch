import os
import tkinter as tk
from tkinter import ttk

# 設定資料夾路徑
log_directory = '/var/local/log/cms/ScoringService-0'

# 創建視窗
root = tk.Tk()
root.title("選擇要讀取的 .log 檔案")

# 獲取該資料夾中所有的 .log 檔案
log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]

# 下拉選單
def on_select(event):
    # 當選擇一個檔案時，讀取並過濾內容
    filename = log_files_combobox.get()
    file_path = os.path.join(log_directory, filename)

    # 檢查檔案是否存在
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            for line in file:
                # 只處理包含 'INFO [Scoring,0 8 ScoringService::execute]' 或 'INFO [Scoring,0 8 triggeredservice::run] Executing operation' 的行
                if 'INFO [Scoring,0 8 ScoringService::execute]' in line or 'INFO [Scoring,0 8 triggeredservice::run] Executing operation' in line:
                    print(line.strip())  # 移除前後空白並顯示該行
    else:
        print(f"檔案 {filename} 不存在或不是 .log 檔案")

# 創建下拉選單
log_files_combobox = ttk.Combobox(root, values=log_files)
log_files_combobox.set("請選擇 .log 檔案")  # 預設顯示文字
log_files_combobox.bind("<<ComboboxSelected>>", on_select)  # 綁定選擇事件
log_files_combobox.pack(pady=20)

# 開始主迴圈
root.mainloop()
