# CMS減肥  
  
目的:備份完比完賽的CMS，自動清理使用者紀錄，讓下一次考試可以直接有乾淨版本可以直接使用  

## cmsRemoveParticipation  
  
指令程式碼位置:/usr/local/lib/python3.10/dist-packages/cms-1.5.dev0-py3.10.egg/cmscontrib/RemoveParticipation.py  
  
刪除資料庫中的participations 
  
![image](https://github.com/user-attachments/assets/a4de4aef-f2e6-478d-8ace-14a1d82ba3bc) 
  
刪除Ranking紀錄及Question的紀錄  
  
```
for i in $(seq -w 1 75); do
  cmsRemoveParticipation -c 1 S$i
done
```
*他跟Contest的已加入User綁在一起，考試的已加入user會被刪除，所以考試需要重新加入User  
```
for i in $(seq -w 1 75); do
  cmsAddParticipation -c 1 S$i
done
```
MYClean.sh可以自動化全部刪除及重新加入使用者  

## Shell Script  
給權限不然不能執行  
```
chmod +x MYClean.sh
```
執行  
```
./MYClean.sh
```
