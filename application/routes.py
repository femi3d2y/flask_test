from flask import render_template 
from application import app

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=dummyData)
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/login')
def login():
    return render_template('login.html', title='Login')

dummyData = [
        {
            "name": {"first":"Leeroy", "last":"Jenkins"},
            "title":"First Post",
            "content":"This is some dummy data for Flask lectures"
        },
        {
            "name": {"first":"Matthew", "last":"Patel"},
            "title":"Second Post",
            "content":"This is even more dummy data for Flask lectures"
        }
    ]
