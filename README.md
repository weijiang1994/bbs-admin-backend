## BBS-Admin-Backend

### Start
[中文](README-ZH.md)

At first, clone the repository to your computer with below command.
```shell
git clone https://github.com/weijiang1994/bbs-admin-backend.git
```
Then configure the runtime environment with below command.
```shell
cd bbs-admin-backend
cp resources/conf.example.yaml resources/conf.yml
pip install -r requirments.txt
vim .env
```
Input below content to the .env file.
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
Run serve with below command
```shell
flask run --port 8008
```