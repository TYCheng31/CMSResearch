# cmsRemoveParticipation  
## 刪除Ranking紀錄及Question的紀錄  
### 他跟Contest的已加入User綁在一起，所以考試需要重加入User
```
yes | for i in $(seq -w 1 75); do
  cmsRemoveParticipation -c 1  S$i
done
```
