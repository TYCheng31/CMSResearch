import os
import re
import tkinter as tk
from tkinter import ttk
import pandas as pd

# 設定資料夾路徑
log_directory = '/var/local/log/cms/ScoringService-0'

# 創建視窗
root = tk.Tk()
root.title("選擇要讀取的 .log 檔案並輸出 Excel")

# 獲取該資料夾中所有的 .log 檔案
log_files = [f for f in os.listdir(log_directory) if f.endswith('.log')]

def on_select(event):
    # 當選擇一個檔案時，讀取並處理內容
    filename = log_files_combobox.get()
    file_path = os.path.join(log_directory, filename)

    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"檔案 {filename} 不存在或不是 .log 檔案")
        return

    data = []  # 用來儲存 [DateTime, Submission, Seconds] 的資料
    with open(file_path, 'r') as file:
        lines = file.readlines()
        # 遍歷所有行，當找到 triggeredservice 行時，檢查下一行是否為 execute 行
        for i in range(len(lines)):
            line = lines[i]
            if 'triggeredservice::run' in line:
                # 抓取行首的日期與時間
                datetime_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d+)', line)
                datetime_value = datetime_match.group(1) if datetime_match else ""
                # 使用正則表達式抓取 submission 編號
                match_submission = re.search(r'scoring submission (\d+)', line)
                if match_submission:
                    submission = match_submission.group(1)
                    # 檢查下一行是否為 scoring execute 行
                    if i + 1 < len(lines) and 'ScoringService::execute' in lines[i+1]:
                        match_seconds = re.search(r'Submission scored ([0-9.]+) seconds', lines[i+1])
                        if match_seconds:
                            seconds = match_seconds.group(1)
                            data.append([datetime_value, submission, seconds])
    
    if data:
        # 建立 DataFrame，並輸出成 Excel 檔案
        df = pd.DataFrame(data, columns=['DateTime', 'Submission', 'Seconds'])
        # 輸出檔名與原始 log 檔名相同，但副檔名改為 .xlsx
        output_file = os.path.splitext(filename)[0] + '.xlsx'
        output_path = os.path.join(log_directory, output_file)
        df.to_excel(output_path, index=False)
        print(f"結果已存成 Excel 檔案：{output_path}")
    else:
        print("沒有找到符合條件的資料。")

# 創建下拉選單
log_files_combobox = ttk.Combobox(root, values=log_files)
log_files_combobox.set("請選擇 .log 檔案")  # 預設顯示文字
log_files_combobox.bind("<<ComboboxSelected>>", on_select)  # 綁定選擇事件
log_files_combobox.pack(pady=20)

# 開始主迴圈
root.mainloop()
