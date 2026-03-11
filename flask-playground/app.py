from flask import Flask
from flask import request
from flask import url_for

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
    
def do_the_login():
    return 'lol'
    
def show_the_login_form():
    return 'form'