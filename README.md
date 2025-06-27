# CMS 安裝步驟 ( Ubuntu24.04LTS )
裝置:Raspberry Pi 4B 、 Raspberry Pi 5  
官方下載文件 : https://cms.readthedocs.io/en/v1.5/Installation.html
### 安裝核心開發工具與 PostgreSQL
```
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    openjdk-11-jdk-headless \
    fp-compiler \
    postgresql \
    postgresql-client \
    cppreference-doc-en-html \
    cgroup-lite \
    libcap-dev \
    zip
```
<details>
    <summary>📂說明各套件用途</summary>
    
```
build-essential            # GNU C/C++ 編譯工具集合（gcc、g++、make 等），用於編譯原始碼和建置 C/C++ 程式。 
openjdk-11-jdk-headless    # Java 11 開發環境（不含圖形介面支援），提供 javac、java 等命令，用於編譯並執行 Java 應用程式。 
fp-compiler                # Free Pascal 編譯器，支援編譯 Pascal 語言程式，常用於競賽或教學環境。 
postgresql                 # PostgreSQL 資料庫伺服器，提供關聯式資料庫服務，用於儲存和管理應用程式資料。 
postgresql-client          # PostgreSQL 客戶端工具（如 psql），用於遠端或本地連線、查詢和管理 PostgreSQL 資料庫。 
cppreference-doc-en-html   # C/C++ 標準函式庫參考文件（HTML 格式），方便在離線環境下查閱 C++ 標準庫 API。 
cgroup-lite                # 簡化版 cgroup v2 管理程式，用於在 Linux 上做資源（CPU、記憶體、I/O）限制與隔離。 
libcap-dev                 # 權限能力（capabilities）程式庫開發頭檔，讓程式可使用細粒度的 Linux 能力管理功能。 
zip                        # 檔案壓縮工具，用於將多個檔案或目錄打包並壓縮成 .zip 格式。 
```
</details>

### 安裝 Python 開發 headers 與資料庫介面
```
sudo apt-get install -y \
    python3.12-dev \
    libpq-dev \
    libcups2-dev \
    libyaml-dev \
    libffi-dev \
    python3-pip
```
<details>
    <summary>📂說明各套件用途</summary>
    
```
python3.12-dev    # Python 3.12 的開發套件，包含標頭檔與靜態庫，用於編譯需呼叫 Python C API 的擴充模組。 
libpq-dev         # PostgreSQL 客戶端開發庫，提供 libpq API 與標頭，讓程式能編譯並連接到 PostgreSQL 資料庫。 
libcups2-dev      # CUPS（Common UNIX Printing System）開發套件，包含列印伺服器與列印驅動程式的標頭與函式庫，用於開發列印功能。 
libyaml-dev       # YAML 解析器開發套件，提供 libyaml 函式庫與標頭，讓程式能讀寫 YAML 格式檔案。 
libffi-dev        # FFI（Foreign Function Interface） 開發套件，包含標頭與靜態庫，允許在執行期呼叫動態載入的 C 函式，常用於 Python、Ruby 等語言擴充。 
python3-pip       # Python 3 的套件管理工具 pip，用於安裝、升級與管理 Python 第三方套件。 
 
```
</details>

### 從 github clone CMS的檔案
CMS官方github: https://github.com/cms-dev/cms.git
```
sudo apt install git
git clone https://github.com/cms-dev/cms.git --recursive
cd cms
```
### 執行前置安裝腳本
用途是當cms在執行需要權限去讀寫檔案時(ex:/usr/etc/log)，加入群組的用戶可以以低權限執行。
沒有執行的話會讓cms在安裝自己的log檔案的時候，會因為權限不足而沒辦法正常創建。
加入群組完要重啟
```
sudo python3 prerequisites.py install
sudo reboot
```
回答 Y 可讓腳本自動加進 cmsuser 群組
### 建立並啟用 Python 虛擬環境
```
sudo apt install python3.12-venv
python3 -m venv ~/cms_venv
```
### 進入虛擬環境
```
source ~/cms_venv/bin/activate
```
### 安裝 Python 相依套件
```
cd cms
pip3 install -r requirements.txt
```
### 安裝 CMS 本體
```
python3 setup.py install
```
### 進入資料庫設定
```
sudo su - postgres
```
### 建立資料庫名稱、使用者、使用者密碼(需要輸入)
```
createuser --username=postgres --pwprompt cmsuser
createdb --username=postgres --owner=cmsuser cmsdb
psql --username=postgres --dbname=cmsdb --command='ALTER SCHEMA public OWNER TO cmsuser'
psql --username=postgres --dbname=cmsdb --command='GRANT SELECT ON pg_largeobject TO cmsuser'

logout
```
### 更改cms.conf設定
把cms.conf這行:
"database":"postgresql+psycopg2://cmsuser:your_password@localhost:5432/cmsdb"
your_password->改成上一步驟自己設定的密碼
```
sudo nano /usr/local/etc/cms.conf
```
### 初始化資料庫
要使用CMS的指令都必須在/cms_venv/bin目錄下執行
可以輸入ls查看所有指令
```
cd ~/cms_venv/bin
cmsInitDB
```
### 創建管理介面使用者
PASSWORD->設定成自己的密碼
NAME->改成自己的名字
```
cmsAddAdmin -p PASSWORD NAME
```
### 進入CMS管理介面
```
cmsAdminWebServer
```
進入管理介面可以新增考試
### 開啟考試
```
cmsResourceService -a
```

