# app.py
from flask import Flask, render_template, request, redirect, url_for
import os
import csv
from process_data import process_data  # 1) 引入你剛定義的函式

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    csv_data = None

    # 2) 設定生成的 CSV 路徑 (需與 process_data.py 裡一致)
    csv_full_path = os.path.join('/home/cms/my_flask_app/static', 'aggregated_output.csv')

    if os.path.exists(csv_full_path):
        with open(csv_full_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            csv_data = list(reader)

    return render_template('index.html', csv_data=csv_data)

@app.route('/run', methods=['POST'])
def run_script():
    try:
        # 3) 按下按鈕後，執行你的資料處理程式
        process_data()
        # 執行完後，重新導向回 index()，顯示更新後的 CSV
        return redirect(url_for('index'))
    except Exception as e:
        return f"執行程式時發生錯誤: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)

