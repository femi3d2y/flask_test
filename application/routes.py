from flask import render_template, redirect, url_for 
from application.forms import PostForm
from application import app, db
from application.models import Posts

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
@app.route('/post', methods=['GET','POST'])
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        title=form.title.data,
        content=form.content.data
    )
                
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('post.html', title='Post', form=form)

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
