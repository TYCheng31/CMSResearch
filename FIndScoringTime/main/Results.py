import subprocess
import time
import os
def run_python_scripts():
    # 指定要執行的 Python 檔案
    first_script = "/findPY/findDB.py"  # 替換為第一個 Python 檔案的路徑
    second_script = "/findPY/findLOG.py"  # 替換為第二個 Python 檔案的路徑

    # 執行第一個 Python 檔案
    print(f"正在執行 {first_script} ...")
    subprocess.run(["python3", first_script])  # 等待直到第一個檔案執行完成

    # 檢查是否第一個檔案已經輸出 CSV，這裡假設輸出檔案是 "findDB.csv"
    csv_output_path = "/csvData/findDB.csv"
    while not os.path.exists(csv_output_path):
        print("等待 CSV 檔案生成中...")
        time.sleep(2)  # 每 2 秒檢查一次

    # 執行第二個 Python 檔案
    print(f"正在執行 {second_script} ...")
    subprocess.run(["python3", second_script])  # 執行第二個檔案

    print("兩個 Python 檔案已成功執行！")

if __name__ == "__main__":
    run_python_scripts()

