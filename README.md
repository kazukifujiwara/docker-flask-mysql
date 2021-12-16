# docker-flask-mysql

## Containers

```
(app_nginx) -- (app_flask) -- (app_mysql)

IMAGE                    COMMAND                  PORTS                 NAMES
nginx:latest             "/docker-entrypoint.…"   0.0.0.0:80->80/tcp    app_nginx
docker-flask-mysql_app   "uwsgi --ini /app/ap…"                         app_flask
app_mysql                "docker-entrypoint.s…"   3306/tcp, 33060/tcp   app_mysql
```

## Create admin user

```
docker exec -it app_mysql /bin/bash
mysql -uroot -p
(enter password: root(default))
update user set admin=true where username="admin";
```

## Component

```
.
├── README.md
├── docker-compose.yml
├── app
│   ├── Dockerfile
│   └── src
│       ├── app.ini
│       ├── app.py
│       ├── requirements.txt
│       ├── templates
│       │   ├── index.html
│       │   └── layout.html
│       └── wsgi.py
├── mysql
│   ├── Dockerfile
│   ├── db
│   │   └── (empty)
│   ├── initdb.d
│   │   └── init.sql
│   └── my.cnf
└── web
    └── nginx.conf
```

## MySQL Default User Settings

* root/root
* test/test

## 動作確認： flask <-> mysql

```
% docker-compose ps   
  Name                 Command               State          Ports       
------------------------------------------------------------------------
app_flask   uwsgi --ini /app/app.ini         Up                         
app_mysql   docker-entrypoint.sh mysqld      Up      3306/tcp, 33060/tcp
app_nginx   /docker-entrypoint.sh ngin ...   Up      0.0.0.0:80->80/tcp 

% docker exec -it app_flask /bin/bash
root@fb00d7f3f98e:/app# 
root@fb00d7f3f98e:/app# python
Python 3.9.7 (default, Oct 12 2021, 02:54:29) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> import mysql.connector
>>> conn = mysql.connector.connect(user='root', password='root', host='db', database='testdb')                  
>>> conn.is_connected()
True
>>> cur = conn.cursor()
>>> cur.execute('SELECT * FROM test')
>>> cur.fetchall()
[(1, 'test1'), (2, 'test2'), (3, 'test3')]
```

## Create DB

対話モードで作成。init.sqlに書こうかな。。。

```
% docker exec -it app_flask /bin/bash
root@7f3690fb100b:/app# python
Python 3.9.7 (default, Oct 12 2021, 02:54:29) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> from app import db
/usr/local/lib/python3.9/site-packages/flask_sqlalchemy/__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.
  warnings.warn(FSADeprecationWarning(
>>> db.create_all()
```


## Notice 

* mysql内のmy.cnf にて認証方式の変更を行った。
    * [変更前] default-authentication-plugin = caching_sha2_password
    * [変更後] default-authentication-plugin = mysql_native_password
    * mysql-connector で接続するため。

## TODO

* Flask-loginでログイン機能の改善
    * ログイン失敗時の処理
    * adminユーザフラグの追加
* 右上にユーザ設定メニューを作る
* DatabaseのCRUD操作をAPI経由で実行可能にする
* [Flask(jinja2) + vue.js でmustache記法( {{ }} )の衝突回避](https://blog.hysakhr.com/2019/09/14/flaskjinja2-vue-js-%E3%81%A7mustache%E8%A8%98%E6%B3%95-%E3%81%AE%E8%A1%9D%E7%AA%81%E5%9B%9E%E9%81%BF/)
* 初回起動時にadmin userを作成する。
* TodoItem の実装
* CreateTodoList (User ver.)の実装

## Referenece

* [Debianのdockerイメージでmysql-clientが無くてハマった人へ](https://qiita.com/henrich/items/1b7ee2f3a72f8bb29cba)
* [DockerでMySQL8.0の環境構築 & 認証方式変更](https://www.wakuwakubank.com/posts/596-mysql-8-with-docker/)
    * my.cnf の設定を変更した。
* [【docker】db:createすると、Plugin caching_sha2_password could not be loaded...のエラーハマった話](https://qiita.com/tomo-IR/items/224d33f14561e759dd16)
* [Flaskで簡易ブログアプリの作成！データベース操作も~Flask超入門 vol.2~](https://www.youtube.com/watch?v=mW0_60SRr3s)
* [ログイン中のユーザ情報の取得](https://www.osstech.co.jp/~hamano/posts/flask-login-ldap/)