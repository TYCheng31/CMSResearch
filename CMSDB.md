# CMSDB(PostgreSQL)相關指令  

## 進入資料庫  
```  
sudo -u postgres psql
```
  
## 連接到CMS資料庫中    
```  
\c cmsdb;
```
  
## 查看目前資料庫中列表所佔用空間   

```  
SELECT
    relname AS table_name,
    pg_size_pretty(pg_total_relation_size(relid)) AS total_size
FROM
    pg_catalog.pg_statio_user_tables
ORDER BY
    pg_total_relation_size(relid) DESC;
```  
