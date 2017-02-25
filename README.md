# 短连接生成器

## 环境

- python版本：python3.6
- Web服务器：gunicorn
- web框架：flask-0.12
- 数据库：sqlite3
- 其他依赖：具体详见requirements.txt



## 部署

- pip install -r requirements.txt 安装第三方依赖

- 修改star.sh脚本，w是进程数，-b是端口。

```
gunicorn -w 4 -b 127.0.0.1:1122 ShortUrl:app >> log.log&
```



- 配置nginx

 ```
  server {
      listen 80;
      server_name example.org; 

      location / {
          proxy_pass http://127.0.0.1:1122; # 这里是指向 gunicorn host 的服务地址
      }

    }
 ```





## 安装

- 在启动gunicorn之前，执行python3 create_db.py，生成数据库。
- 启动gunicorn，访问，域名+'/install'进行安装。

