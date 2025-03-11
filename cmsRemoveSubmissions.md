# cmsRemoveSubmissions  
  
指令程式碼位置:/usr/local/lib/python3.10/dist-packages/cms-1.5.dev0-py3.10.egg/cmscontrib/RemoveSubmissions.py  

##刪除資料
1.刪除資料庫中的submissions,submission_results,submission_files  

2.刪除/var/local/lib/cms/submissions資料夾中每一位user的繳交資料  
  
![image](https://github.com/user-attachments/assets/a4de4aef-f2e6-478d-8ace-14a1d82ba3bc)  

## 刪除單一使用者繳交紀錄  
-c要刪除的Contest ID  
-u要刪除的User ID  
```  
sudo cmsRemoveSubmissions -c 8 -u S01  
``` 
![image](https://github.com/user-attachments/assets/c3cfa183-0781-468e-ada3-e0bf263de8d6)  
## 批量刪除(但是需要一個一個按Y確定)  
```
for i in $(seq -w 1 75); do
  sudo cmsRemoveSubmissions -c 8 -u S$i
done

```
## 可以改用以下每次執行自動輸出Y  
```
yes | for i in $(seq -w 1 75); do
  sudo cmsRemoveSubmissions -c 8 -u S$i
done
```
![image](https://github.com/user-attachments/assets/c0158a8d-1f17-43fd-8908-6cd4d5f149c8)  



