# docker-flask-mysql

## TODO

* app_mysql, app_flask の接続テスト
* Flask-loginでログイン機能を実装する

## Component

```
TODO:treeを実行する
```



```
from flask import Flask, request, jsonify
import mysql.connector

conn = mysql.connector.connect(
    host = 'app_mysql',
    port = 3306,
    user = 'test',
    password = 'test',
    database = 'testdb',
)

conn.ping(reconnect=True)
cur = conn.cursor()
cur.execute('SELECT * FROM test')
sql_result = cur.fetchall()
```

## Commands

## Referenece

* [Debianのdockerイメージでmysql-clientが無くてハマった人へ](https://qiita.com/henrich/items/1b7ee2f3a72f8bb29cba)