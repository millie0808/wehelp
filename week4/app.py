from flask import Flask, render_template, request, redirect, url_for, session

app=Flask(__name__)
app.secret_key = 'secret secret key'

@app.route('/', methods=['GET','POST'])
def index():
    session['SIGNED-IN'] = False
    if request.method == 'POST':
        if request.values['send'] == '登入':
            session['account']=request.form.get('account')
            session['password']=request.form.get('password')
            return redirect(url_for('signin'))
    else:
	    return render_template('home.html')

@app.route('/signin')
def signin():
    account = session.get('account') 
    password = session.get('password')
    if account == "" or password == "":
        return redirect(url_for('login_error', message='請輸入帳號密碼'))
    elif account == 'test' and password == 'test':
        session['SIGNED-IN'] = True
        return redirect(url_for('login_success'))
    else:
        return redirect(url_for('login_error', message='帳號或密碼輸入錯誤'))

@app.route('/member')
def login_success():
    if session['SIGNED-IN'] == True:
        return render_template('member.html')
    else:
        return redirect(url_for('index'))
    

@app.route('/error')
def login_error():
    error_message = request.args.get('message', '')
    return render_template('error.html',message=error_message)

@app.route('/signout', methods=['GET'])
def signout():
    if request.method == 'GET':
        session['SIGNED-IN'] = False
        return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(port='3000',debug=True)