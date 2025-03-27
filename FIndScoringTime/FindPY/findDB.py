import psycopg2
import pandas as pd

def process_data():
    # 連接資料庫
    conn = psycopg2.connect(
        dbname="cmsdb",
        user="postgres",
        password="0000",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # 查詢 submissions 資料，選取 id 和 task_id
    cur.execute("SELECT id, task_id FROM submissions")
    submissions_data = cur.fetchall()

    # 取得每個 task_id 對應的 name
    task_names = []
    for submission in submissions_data:
        task_id = submission[1]
        cur.execute("SELECT name FROM tasks WHERE id = %s", (task_id,))
        task_data = cur.fetchone()
        task_name = task_data[0] if task_data else "Unknown"  # 如果找不到對應的 task_name，設為 "Unknown"
        task_names.append(task_name)

    # 將資料轉換為 pandas DataFrame，包含 id, task_id 和 task_name
    submissions_df = pd.DataFrame(submissions_data, columns=["id", "task_id"])
    submissions_df["task_name"] = task_names  # 加入 task_name 欄位

    # 設定 CSV 檔案路徑
    csv_path = "/home/cms/Desktop/FIndScoringTime/FindPY/csvData/findDB.csv"

    # 將資料匯出為 CSV
    submissions_df.to_csv(csv_path, index=False, encoding="utf-8")

    print(f"submissions 資料已成功匯出到：{csv_path}")

    # 關閉資料庫連接
    cur.close()
    conn.close()

# 呼叫處理函式
process_data()

