import os
import re
import tkinter as tk
from tkinter import filedialog
import csv
import pandas as pd
import matplotlib.pyplot as plt

# 正則表達式提取資料
submission_pattern = r"Executing operation `scoring submission (\d+) on dataset (\d+)'"
scored_pattern = r"Submission scored ([\d\.]+) seconds after submission"

# 建立GUI介面讓使用者選擇檔案
def select_log_file():
    # 開啟檔案選擇對話框
    file_path = filedialog.askopenfilename(
        title="Select a log file", 
        filetypes=(("Log files", "*.log"), ("All files", "*.*"))
    )
    if file_path:
        extract_info_from_log(file_path)

# 從選擇的log檔案中提取資訊並輸出至CSV
def extract_info_from_log(log_file_path):
    # 讀取 findDB.csv，這包含 task_id 和 task_name
    task_data_csv = "/home/cms/Desktop/FIndScoringTime/FindPY/csvData/findDB.csv"  # 替換為您的 findDB.csv 檔案路徑
    task_df = pd.read_csv(task_data_csv)

    # 提取 findDB.csv 的路徑，以便將輸出的 CSV 儲存到相同的目錄
    output_directory = os.path.dirname(task_data_csv)
    
    # 開啟CSV文件，準備寫入資料
    csv_filename = os.path.basename(log_file_path).replace('.log', '_output.csv')
    output_csv_path = os.path.join(output_directory, csv_filename)

    task_scores = []  # 用來儲存每個 task_name 和其對應的 scored_time
    
    # 開啟 log 檔案並逐行讀取
    with open(log_file_path, 'r') as file:
        lines = file.readlines()

        # 迴圈逐行處理
        for i in range(len(lines)):
            line = lines[i]
            # 如果該行匹配到 submission pattern
            match_submission = re.search(submission_pattern, line)
            if match_submission:
                submission_id = match_submission.group(1)
                dataset_id = match_submission.group(2)

                # 根據 dataset_id 查找對應的 task_name
                # 確保資料型別一致，將 dataset_id 和 task_id 都轉換為字串型別
                dataset_id_str = str(dataset_id)
                task_name = task_df.loc[task_df['task_id'].astype(str) == dataset_id_str, 'task_name'].values
                task_name = task_name[0] if len(task_name) > 0 else "Unknown"

                # 接著讀取下一行，看是否匹配到 scored pattern
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    match_score = re.search(scored_pattern, next_line)
                    if match_score:
                        scored_time = float(match_score.group(1))  # 確保為浮點數型別
                        
                        # 儲存每個 task_name 和 scored_time
                        task_scores.append({
                            'Task Name': task_name,
                            'Scored Time': scored_time
                        })
    
    # 將資料轉換為 DataFrame
    task_df = pd.DataFrame(task_scores)

    # 計算每個 task_name 的平均 scored time
    avg_task_scores = task_df.groupby('Task Name')['Scored Time'].mean().reset_index()

    # 輸出結果到新的 CSV 檔案
    avg_csv_filename = os.path.basename(log_file_path).replace('.log', '_avg_output.csv')
    avg_output_csv_path = os.path.join(output_directory, avg_csv_filename)
    avg_task_scores.to_csv(avg_output_csv_path, index=False)

    print(f"Output saved to {avg_output_csv_path}")
    
    # 繪製圖表顯示
    plot_avg_scores(avg_task_scores)

# 顯示圖表
def plot_avg_scores(avg_task_scores):
    # 使用 matplotlib 顯示圖表
    plt.figure(figsize=(10, 6))
    bars = plt.bar(avg_task_scores['Task Name'], avg_task_scores['Scored Time'], color='skyblue')
    plt.xlabel('Task Name')
    plt.ylabel('Average Scored Time (seconds)')
    plt.title('Average Scored Time for Each Task')
    plt.xticks(rotation=90)  # 讓任務名稱顯示得清晰
    plt.tight_layout()

    # 在每個柱子上顯示數字
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 2), ha='center', va='bottom')

    plt.show()

# 主程式設定
def main():
    # 設定 Tkinter 視窗
    root = tk.Tk()
    root.withdraw()  # 隱藏主視窗

    # 呼叫檔案選擇對話框
    select_log_file()

if __name__ == "__main__":
    main()

