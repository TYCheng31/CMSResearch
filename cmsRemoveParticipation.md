# cmsRemoveParticipation  
  
指令程式碼位置:/usr/local/lib/python3.10/dist-packages/cms-1.5.dev0-py3.10.egg/cmscontrib/RemoveSubmissions.py  
  
刪除資料庫中的submissions,submission_results,submission_files  
  
![image](https://github.com/user-attachments/assets/a4de4aef-f2e6-478d-8ace-14a1d82ba3bc) 
  
刪除Ranking紀錄及Question的紀錄  
  
### 他跟Contest的已加入User綁在一起，所以考試需要重加入User
```
yes | for i in $(seq -w 1 75); do
  cmsRemoveParticipation -c 1  S$i
done
```
