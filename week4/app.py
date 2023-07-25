from flask import Flask, render_template, request, redirect, url_for, session

app=Flask(__name__,static_folder="static",static_url_path="/")
app.secret_key = 'secret secret key'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signin', methods=['POST'])
def signin():
    account = request.form.get('account')
    password = request.form.get('password')
    if account == "" or password == "":
        session['SIGNED-IN'] = False
        return redirect(url_for('login_error', message='請輸入帳號密碼'))
    elif account == 'test' and password == 'test':
        session['SIGNED-IN'] = True
        return redirect(url_for('login_success'))
    else:
        session['SIGNED-IN'] = False
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
    session['SIGNED-IN'] = False
    return redirect(url_for('index'))

@app.route('/square/<pNumber>')
def square(pNumber):
    pNumber = int(pNumber)
    result = pNumber * pNumber
    return render_template('result.html',result=result)


if __name__ == '__main__':
	app.run(port='3000',debug=True)