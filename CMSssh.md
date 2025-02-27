# 使用Putty遠端連線Ubuntu24.04  
先更新所有套件  
```
apt update
apt upgrade  
```
下載openssh-server  
```
apt install openssh-server
```
設定config中參數 
```
nano /etc/ssh/sshd_config
```
找到目前ip位置  
```
ip addr show
```
進到Putty連線  
![image](https://github.com/user-attachments/assets/fb525f55-ea9c-4e1a-bb29-c62b14ae2096)  
用Ubuntu的帳號登入  
![image](https://github.com/user-attachments/assets/062369cf-ddb2-446c-aaef-fd8957f3c5f6)
