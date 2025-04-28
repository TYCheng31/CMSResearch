# 計算CMS各題目計算分數時間的方法  
## 1.找到.log檔位置:/var/local/log/cms/ScoringService-0查看submission_id/dataset_id/time  
FndPY中的findLOG.py負責執行  
![image](https://github.com/user-attachments/assets/63e50b1e-3e2b-4ac0-93e1-523a9d68481c)  
## 2.分析資料庫後進行關聯查詢  
FndPY中的findDB.py負責執行   
![image](https://github.com/user-attachments/assets/b9b65410-b15e-4a18-8467-ff08e38632d5)
## 3.選擇日誌後自動化輸出平均時間圖片  
main的Results.py負責執行  
![image](https://github.com/user-attachments/assets/465778b8-a5cb-4865-8877-198c9991837c)
![image](https://github.com/user-attachments/assets/9fc1a1b3-b2cb-4843-a33a-8b71eee80ab7)

