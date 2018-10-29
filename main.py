from flask import Flask, request, redirect, render_template
import jinja2, re

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

    # Initialize strings as global empty strings
    global username_error, password_error, verify_password_error, email_error
    username_error = ''
    password_error = ''
    verify_password_error = ''
    email_error = ''
    
    # Validate form values 
    if not validate(username, password, verify_password, email):
        return redirect("/?username_error={0}&password_error={1}&verify_password_error={2}&email_error={3}&username={4}&email={5}".format(username_error, password_error, verify_password_error, email_error, username, email))
    else:
        return render_template('welcome.html', username=username, password=password, verify_password=verify_password, email=email)


# Validate form function
def validate(username, password, verify_password, email):
    # Regex validation:
    # String can be any set of characters of length 3-20 excluding any whitespace characters
    valid = re.compile(r'^[^\s]{3,20}$')
    # Email string must have basic email form and one and only one '@' and one and only one '.'
    email_valid = re.compile(r'[^@.]+@[^@.]+\.[^@.]+$')

    # Initialize error variables as global
    global username_error, password_error, verify_password_error, email_error

    # Validate each form field for length, whitespace, matching passwords, and email form
    if not valid.match(username):
        username_error = "That's not a valid username"
    if not valid.match(password):
        password_error = "That's not a valid password"
    if email != "":
        if not email_valid.match(email) or not valid.match(email):
            email_error = "That's not a valid email"
    if password != verify_password:
         verify_password_error = "Passwords do not match"
    if username_error or password_error or verify_password_error or email_error:
        return False
    else:
        return True


app.run()