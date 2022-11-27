from flask import render_template
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dmitry'} # mock user
    posts = [
        {
            'author': {'username': 'Robin'},
            'body': 'Hi from Leuvenford!'
        },
        {
            'author': {'username': 'Gavain'},
            'body': 'Hi'
        }
    ]
    return render_template('index.html', title='Home', user=user)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)