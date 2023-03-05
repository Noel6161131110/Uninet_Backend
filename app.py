from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

# Initialising flask app
app = Flask(__name__)

# Configuring connection to MySQL Server with flask using flask_mysqldb library
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uninet'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Establishing connection to MySQL Server with flask using flask_mysqldb library
mysql = MySQL(app)

from controller.user_Auth import userAuth_api  # User Authentication related library

from controller.searchBox import searchBox_api  # User Authentication related library

from controller.user_posts import userPost_api

app.register_blueprint(userPost_api)

app.register_blueprint(userAuth_api)

app.register_blueprint(searchBox_api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,debug=True)