from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector

app=Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)
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
    cursor.execute("""SELECT username 
                      FROM member
                      WHERE username=%s;
                   """,(username,))
    query_result = cursor.fetchone()
    if query_result:
        return redirect(url_for('error', message='帳號已被註冊'))
    else:
        sql = """INSERT INTO member(name,username,password) 
                 VALUES (%s,%s,%s);
              """
        cursor.execute(sql, (name, username, password))
        mydb.commit()
        cursor.close()
        return redirect(url_for('index'))


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('usernameIn')
    password = request.form.get('passwordIn')
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""SELECT id,name,username,password 
                      FROM member 
                      WHERE username=%s AND 
                            password=%s;
                   """,(username, password))
    query_result = cursor.fetchone()
    cursor.close()
    if query_result == None:
        return redirect(url_for('error', message='帳號或密碼輸入錯誤'))
    else:
        session['id'] = query_result['id']
        session['name'] = query_result['name']
        session['username'] = query_result['username']
        return redirect(url_for('member'))

@app.route('/member')
def member():
    if 'id' in session:
        user_name = session['name']
        user_id = session['id']
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("""SELECT message.*,member.name 
                          FROM message 
                          LEFT JOIN member 
                          ON message.member_id=member.id;
                       """)
        all_message = cursor.fetchall()
        cursor.close()
        return render_template('member.html', all_message=all_message)
    else:
        return redirect(url_for('index'))

@app.route('/api/member', methods=['GET','PATCH'])
def api_member():
    if 'id' in session:
        if request.method == 'GET':
            username = request.args.get('username', '')
            cursor = mydb.cursor(dictionary=True)
            cursor.execute("""SELECT id,name,username
                              FROM member
                              WHERE username=%s;
                           """,(username,))
            query_result = cursor.fetchone()
            cursor.close()
            if query_result:
                return jsonify({"data":query_result})
            else:
                return jsonify({"data":None})
        if request.method == 'PATCH':
            data = request.get_json()
            new_name = data.get('name')
            cursor = mydb.cursor()
            sql = """UPDATE member
                     SET name=%s
                     WHERE id=%s;
                  """
            try:
                cursor.execute(sql, (new_name, session['id']))
                mydb.commit()
                cursor.close()
                session['name'] = new_name
                return jsonify({"ok":True})
            except:
                mydb.rollback()
                return jsonify({"error":True})
    else:
        return redirect(url_for('index'))

@app.route('/error')
def error():
    error_message = request.args.get('message', '')
    return render_template('error.html', message=error_message)

@app.route('/signout', methods=['GET'])
def signout():
    session.pop('id', None)
    session.pop('name', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/createMessage', methods=['POST'])
def createMessage():
    if 'id' in session:
        message = request.form.get('message')
        cursor = mydb.cursor()
        cursor.execute("""INSERT INTO message(member_id,content) 
                          VALUES (%s,%s);
                       """,(session['id'], message))
        mydb.commit()
        cursor.close()
        return redirect(url_for('member'))
    else:
        return redirect(url_for('index'))

@app.route('/deleteMessage', methods=['POST'])
def deleteMessage():
    if 'id' in session:
        message_id = request.form.get('messageID')
        cursor = mydb.cursor()
        cursor.execute("""DELETE FROM message 
                          WHERE id=%s
                       """,(message_id,))
        mydb.commit()
        cursor.close()
        return redirect(url_for('member'))
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(port='3000', debug=True)