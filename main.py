from flask import Flask, request, redirect, render_template
import jinja2, re, cgi

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/')
def index():
    # Parse parameters
    global username_error, password_error, verify_password_error, email_error
    username_error = request.args.get('username_error')
    password_error = request.args.get('password_error')
    verify_password_error = request.args.get('verify_password_error')
    email_error = request.args.get('email_error')
    username = request.args.get('username', default='')
    email = request.args.get('email', default='')

    return render_template('index.html', username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error, username=username, email=email)



@app.route('/welcome', methods=['POST'])
def welcome():
    # Parse parameters
    username = request.form['username']
    password = request.form['password']
    verify_password = request.form['verify_password']
    email = request.form.get('email')

    # Initialize strings with empty strings
    global username_error, password_error, verify_password_error, email_error
    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''
    
    if not validate(username, password, verify_password, email):
        return redirect("/?username_error={0}&password_error={1}&verify_password_error={2}&email_error={3}&username={4}&email={5}".format(username_error, password_error, verify_password_error, email_error, username, email))
    else:
        return render_template('welcome.html', username=username, password=password, verify_password=verify_password, email=email)

# Validate form
def validate(username, password, verify_password, email):
    global username_error, password_error, verify_password_error, email_error
    if username == "":
        username_error = "That's not a valid username"
    if password == "":
        password_error = "That's not a valid password"
    if verify_password == "":
        verify_password_error = "Passwords do not match"
    if "x" in username:
        username_error = "x"
    if password != verify_password:
        verify_password_error = "Passwords do not match"
    if email == "x":
        email_error = "That's not a valid email"
    if username_error or password_error or verify_password_error or email_error:
        return False
    else:
        return True

app.run()