from flask import render_template, redirect, url_for, request 
from application.forms import PostForm, RegistrationForm, LoginForm
from application import app, db, bcrypt
from application.models import Posts, Users
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home', posts=dummyData)
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

   # def set_password(self, password):
       # password_hash = bcrypt.hashpassword(password.encode('utf8'), bcrypt.gensalt())
       # self.password_hash = password_hash.decode('utf8')

    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
    

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
        

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))

    return render_template('login.html', title='Login', form=form)
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
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)


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
