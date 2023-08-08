from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app=Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key = 'secret secret key'

mydb = mysql.connector.connect(
  host="localhost",
  database="website",
  user="root",
  password="rootpass"
)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form.get('name')
    username = request.form.get('usernameUp')
    password = request.form.get('passwordUp')
    cursor = mydb.cursor()
    cursor.execute("SELECT username FROM member WHERE username=%s;",(username,))
    query_result = cursor.fetchone()
    if query_result:
        return redirect(url_for('error', message='帳號已被註冊'))
    else:
        sql = "INSERT INTO member(name,username,password) VALUES (%s,%s,%s);"
        cursor.execute(sql, (name,username,password))
        mydb.commit()
        cursor.close()
        return redirect(url_for('index'))


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('usernameIn')
    password = request.form.get('passwordIn')
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT id,name,username,password FROM member WHERE username=%s;",(username,))
    #query_result = dict(zip(cursor.column_names, cursor.fetchone()))
    query_result = cursor.fetchone()
    cursor.close()
    if query_result == None:
        session['SIGNED-IN'] = False
        return redirect(url_for('error', message='帳號或密碼輸入錯誤'))
    elif password == query_result['password']:
        session['SIGNED-IN'] = True
        session['id'] = query_result['id']
        session['name'] = query_result['name']
        session['username'] = query_result['username']
        return redirect(url_for('member'))
    else:
        session['SIGNED-IN'] = False
        return redirect(url_for('error', message='帳號或密碼輸入錯誤'))

@app.route('/member')
def member():
    if session['SIGNED-IN'] == True:
        member_name = session['name']
        member_id = session['id']
        # 獲取資料庫table message
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT message.*,member.name FROM message LEFT JOIN member ON message.member_id=member.id;")
        all_message = cursor.fetchall()
        cursor.close()
        return render_template('member.html',member_name=member_name,member_id=member_id,all_message=all_message)
    else:
        return redirect(url_for('index'))

@app.route('/error')
def error():
    error_message = request.args.get('message', '')
    return render_template('error.html',message=error_message)

@app.route('/signout', methods=['GET'])
def signout():
    session['SIGNED-IN'] = False
    del session['id']
    del session['name']
    del session['username']
    return redirect(url_for('index'))


@app.route('/createMessage', methods=['POST'])
def createMessage():
    message = request.form.get('message')
    cursor = mydb.cursor()
    cursor.execute("INSERT INTO message(member_id,content) VALUES (%s,%s);",(session['id'],message))
    mydb.commit()
    cursor.close()
    return redirect(url_for('member'))

@app.route('/deleteMessage', methods=['POST'])
def deleteMessage():
    message_id = request.form.get('messageID')
    cursor = mydb.cursor()
    cursor.execute("DELETE FROM message WHERE id=%s",(message_id,))
    mydb.commit()
    cursor.close()
    return redirect(url_for('member'))

    
    

if __name__ == '__main__':
	app.run(port='3000',debug=True)