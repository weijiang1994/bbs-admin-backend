## BBS-Admin-Backend

### 开始
[English](README.md)

首先通过下面的命令克隆仓库到你的本地
```shell
git clone https://github.com/weijiang1994/bbs-admin-backend.git
```
然后根据下面的命令配置好运行环境
```shell
cd bbs-admin-backend
cp resources/conf.example.yaml resources/conf.yml
pip install -r requirments.txt
touch .env
```
将下面的内容输入到上面的`.env`文件中去，根据你的实际情况输入。
```dotenv
MAIL_SERVER='your email server support smtp or other protocol'
MAIL_USERNAME='your email '
MAIL_PASSWORD='your email stmp login password'
SECRET_KEY=production
DATABASE_USER= 'database username'
DATABASE_PWD= 'database password'
DATABASE_HOST=127.0.0.1
DATABASE_PORT=3306
```
运行服务
```shell
flask run
```
