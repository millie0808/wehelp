from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool

app=Flask(
    __name__,
    static_folder = "static",
    static_url_path = "/"
)
app.secret_key = 'secret secret key'

mydb = {
    "host": "localhost",
    "database": "website",
    "user": "root",
    "password": "rootpass"
}

connection_pool = MySQLConnectionPool(
    pool_name = "my_connection_pool",
    pool_size = 5,
    **mydb
)

def execute_query(query, params=None, fetch_one=False, fetch_all=False, commit=False):
    connection = connection_pool.get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params)
    if commit:
        connection.commit()
    else:
        result = None
        if fetch_one:
            result = cursor.fetchone()
        elif fetch_all:
            result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result

def is_username_taken(username):
    sql = "SELECT username FROM member WHERE username=%s;"
    query_result = execute_query(sql, (username,), fetch_one=True)
    return query_result is not None

def handle_signup(name, username, password):
    if is_username_taken(username):
        return redirect(url_for('error', message='帳號已被註冊'))
    else:
        sql = "INSERT INTO member(name, username, password) VALUES (%s, %s, %s);"
        execute_query(sql, (name, username, password), commit=True)
        return redirect('/')

def handle_signin(username, password):
    sql = "SELECT id, name, username, password FROM member WHERE username=%s AND password=%s;"
    query_result = execute_query(sql, (username, password), fetch_one=True)
    if query_result is None:
        return redirect(url_for('error', message='帳號或密碼輸入錯誤'))
    else:
        session['id'] = query_result['id']
        session['name'] = query_result['name']
        session['username'] = query_result['username']
        return redirect('/member')


# routes

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    username = request.form.get('usernameUp')
    password = request.form.get('passwordUp')
    return handle_signup(name, username, password)

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('usernameIn')
    password = request.form.get('passwordIn')
    return handle_signin(username, password)

@app.route('/member')
def member():
    if 'id' in session:
        user_name = session['name']
        user_id = session['id']
        sql = """SELECT message.*, member.name 
                 FROM message 
                 LEFT JOIN member ON message.member_id=member.id;"""
        all_message = execute_query(sql, fetch_all=True)
        return render_template('member.html', all_message=all_message)
    else:
        return redirect('/')

@app.route('/api/member', methods=['GET','PATCH'])
def api_member():
    if 'id' in session:
        if request.method == 'GET':
            username = request.args.get('username', '')
            sql = """SELECT id,name,username
                     FROM member
                     WHERE username=%s;"""
            query_result = execute_query(sql, (username,), fetch_one=True)
            if query_result:
                return jsonify({"data":query_result})
            else:
                return jsonify({"data":None})
        if request.method == 'PATCH':
            data = request.get_json()
            new_name = data.get('name')
            sql = """UPDATE member
                     SET name=%s
                     WHERE id=%s;"""
            try:
                execute_query(sql, (new_name, session['id']), commit=True)
                session['name'] = new_name
                return jsonify({"ok":True})
            except:
                connection.rollback()
                connection.close()
                return jsonify({"error":True})
    else:
        return redirect('/')

@app.route('/error')
def error():
    error_message = request.args.get('message', '')
    return render_template('error.html', message=error_message)

@app.route('/signout', methods=['GET'])
def signout():
    session.pop('id', None)
    session.pop('name', None)
    session.pop('username', None)
    return redirect('/')


@app.route('/createMessage', methods=['POST'])
def createMessage():
    if 'id' in session:
        message = request.form.get('message')
        sql = """INSERT INTO message(member_id,content) 
                 VALUES (%s,%s);"""
        execute_query(sql ,(session['id'], message), commit=True)
        return redirect('/member')
    else:
        return redirect('/')

@app.route('/deleteMessage', methods=['POST'])
def deleteMessage():
    if 'id' in session:
        message_id = request.form.get('messageID')
        sql = """DELETE FROM message 
                 WHERE id=%s"""
        execute_query(sql, (message_id,), commit=True)
        return redirect('/member')
    else:
        return redirect('/')


if __name__ == '__main__':
	app.run(port='3000', debug=True)