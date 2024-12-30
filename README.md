# CMSExtend
##這個網頁提供按鈕及時刷新CMS考試時的排名  

## 步驟一：更新系統套件  
```
sudo apt update  
sudo apt upgrade -y  
```
## 步驟二：安裝必要的套件  
### 安裝 Python 及相關工具  
```
sudo apt install python3
python3-pip python3-venv -y  
```
### 安裝 Nginx：  
```
sudo apt install nginx -y  
```
## 步驟三：設定 Python 虛擬環境  
### 建立一個專案目錄my_flask_app  
```
mkdir ~/my_flask_app  
cd ~/my_flask_app  
python3 -m venv venv  
source venv/bin/activate  
```
## 步驟四：安裝 Flask 及其他必要的 Python 套件  
### 在虛擬環境中安裝 Flask 和 Gunicorn  
```
pip install Flask gunicorn  
```
## 步驟五：撰寫 Flask 應用程式  
### 在 my_flask_app 目錄下，建立一個 app.py 檔案  
### 建立 templates 目錄並在其中建立 index.html  
```
mkdir templates
```
### 確保有一個 static/images 目錄來存放生成的圖片  
```
mkdir -p static/images
```
## 步驟六：測試 Flask 應用  
```
python app.py
```
