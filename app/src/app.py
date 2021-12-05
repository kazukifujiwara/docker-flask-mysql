import MySQLdb
from flask import Flask, render_template

app = Flask(__name__)

# app.secret_key = b'random string...'

@app.route('/')
def index():

    # conn = MySQLdb.connect(user='root', passwd='root', host='app_mysql', db='testdb')
    # cur = conn.cursor()
    # sql = "select * test;"
    # cur.execute(sql)

    return render_template('index.html',
        title='Flask Index',
        message='Index'
    )

# Main function is called only when executing ”python app.py”
if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)