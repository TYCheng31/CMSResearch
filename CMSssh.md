# 使用Putty遠端連線Ubuntu24.04  
先更新所有套件  
下載openssh-server  
設定config中參數  
找到目前ip位置
進到Putty連線  
```
apt update  
apt upgrade  
apt install openssh-server
nano /etc/ssh/sshd_config  
ip addr show
```
![image](https://github.com/user-attachments/assets/fb525f55-ea9c-4e1a-bb29-c62b14ae2096)
![image](https://github.com/user-attachments/assets/062369cf-ddb2-446c-aaef-fd8957f3c5f6)
