# process_data.py

import psycopg2
import csv
from datetime import datetime, timedelta

def process_data():
    # 連接資料庫
    conn = psycopg2.connect(
        dbname="cmsdb",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    user_contest_scores = {}

    # 查詢 submission_results 資料，根據 submission_id 獲得 score
    cur.execute("SELECT submission_id, score FROM submission_results")
    submission_results = cur.fetchall()

    for submission_result in submission_results:
        submission_id = submission_result[0]
        score = submission_result[1]

        # 根據 submission_id 查詢 submissions 資料，獲取 participation_id, task_id, timestamp
        cur.execute("SELECT participation_id, task_id, timestamp FROM submissions WHERE id = %s", (submission_id,))
        submission_data = cur.fetchone()
        if submission_data:
            participation_id, task_id, timestamp = submission_data

            # 根據 participation_id 查詢 participations 資料，獲取 contest_id 和 user_id
            cur.execute("SELECT contest_id, user_id FROM participations WHERE id = %s", (participation_id,))
            participation_data = cur.fetchone()
            if participation_data:
                contest_id, user_id = participation_data

                # contest_name, start
                cur.execute("SELECT name, start FROM contests WHERE id = %s", (contest_id,))
                contest_data = cur.fetchone()
                if contest_data:
                    contest_name, contest_start = contest_data
                else:
                    contest_name = "Unknown"
                    contest_start = "Unknown"

                # first_name
                cur.execute("SELECT first_name FROM users WHERE id = %s", (user_id,))
                user_data = cur.fetchone()
                if user_data:
                    first_name = user_data[0]
                else:
                    first_name = "Unknown"

                if (user_id, contest_id) not in user_contest_scores:
                    user_contest_scores[(user_id, contest_id)] = {
                        "first_name": first_name,
                        "contest_name": contest_name,
                        "contest_start": contest_start,
                        "total_score": score,
                        "task_scores": {task_id: score},
                        "timestamps": {task_id: timestamp},
                        "task_earliest_correct": {}
                    }
                    if score == 10:
                        user_contest_scores[(user_id, contest_id)]["task_earliest_correct"][task_id] = timestamp
                else:
                    user_data_dict = user_contest_scores[(user_id, contest_id)]

                    if task_id not in user_data_dict["task_scores"]:
                        user_data_dict["task_scores"][task_id] = score
                        user_data_dict["timestamps"][task_id] = timestamp
                    else:
                        current_score = user_data_dict["task_scores"][task_id]
                        current_timestamp = user_data_dict["timestamps"][task_id]
                        if score > current_score:
                            user_data_dict["task_scores"][task_id] = score
                            user_data_dict["timestamps"][task_id] = timestamp
                        elif score == current_score and timestamp < current_timestamp:
                            user_data_dict["timestamps"][task_id] = timestamp

                    if score == 10:
                        if task_id not in user_data_dict["task_earliest_correct"]:
                            user_data_dict["task_earliest_correct"][task_id] = timestamp
                        else:
                            recorded_timestamp = user_data_dict["task_earliest_correct"][task_id]
                            if timestamp < recorded_timestamp:
                                user_data_dict["task_earliest_correct"][task_id] = timestamp

                    user_data_dict["total_score"] = sum(user_data_dict["task_scores"].values())

    final_results = []

    for (user_id, contest_id), data in user_contest_scores.items():
        latest_timestamp = max(data["timestamps"].values())
        contest_start = data["contest_start"]
        time_difference = latest_timestamp - contest_start
        total_seconds = int(time_difference.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_difference_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        correct_count = len(data["task_earliest_correct"])

        if data["first_name"].startswith("S"):
            final_results.append({
                "first_name": data["first_name"],
                "contest_name": data["contest_name"],
                "contest_start": contest_start.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp": latest_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "total_score": data["total_score"],
                "time_difference_str": time_difference_str,  # 保留字串顯示
                "time_difference_seconds": total_seconds,     # 另外存秒數用於排序
                "correct_count": correct_count
            })

    # ※ 整合相同使用者的結果
    aggregated_results = {}
    for result in final_results:
        first_name = result["first_name"]
        total_score = result["total_score"]
        correct_count = result["correct_count"]
        time_diff_seconds = result["time_difference_seconds"]

        if first_name not in aggregated_results:
            aggregated_results[first_name] = {
                "first_name": first_name,
                "total_score": total_score,
                "time_difference_seconds": time_diff_seconds,
                "correct_count": correct_count
            }
        else:
            aggregated_results[first_name]["total_score"] += total_score
            aggregated_results[first_name]["time_difference_seconds"] += time_diff_seconds
            aggregated_results[first_name]["correct_count"] += correct_count

    # ※ 將整合後的結果轉為列表，並重新計算 time_difference_str
    final_aggregated_results = []
    for data in aggregated_results.values():
        total_seconds = data["time_difference_seconds"]
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_difference_str = f"{hours:02}:{minutes:02}:{seconds:02}"

        final_aggregated_results.append({
            "first_name": data["first_name"],
            "total_score": data["total_score"],
            "correct_count": data["correct_count"],
            "time_difference_str": time_difference_str,
            "time_difference_seconds": total_seconds
        })

    # === 排序規則: 1) total_score 由高到低, 2) correct_count 由高到低, 3) time_difference_seconds 由少到多
    final_aggregated_results_sorted = sorted(
        final_aggregated_results,
        key=lambda x: (
            -x["total_score"],             # 由高到低
            -x["correct_count"],           # 由高到低
             x["time_difference_seconds"]  # 由少到多
        )
    )

    csv_path = "/home/cms/my_flask_app/static/aggregated_output.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as csvfile:
        # 寫入時僅需以下欄位
        fieldnames = ["first_name", "total_score", "correct_count", "time_difference"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in final_aggregated_results_sorted:
            writer.writerow({
                "first_name": result["first_name"],
                "total_score": result["total_score"],
                "correct_count": result["correct_count"],
                "time_difference": result["time_difference_str"]  # 寫入顯示用字串
            })

    cur.close()
    conn.close()

    print(final_aggregated_results_sorted)
    print(f"整合後的 CSV 檔案已生成：{csv_path}")

