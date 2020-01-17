from flask import render_template, redirect, url_for, request, send_file 
from application.forms import PostForm, RegistrationForm, LoginForm, UpdateAccountForm
from application import app, db, bcrypt
from application.models import Posts, Users
from flask_login import login_user, current_user, logout_user, login_required
import os
from s3_demo import download_file, upload_file, list_files

BUCKET ="ifebucket1234" 
UPLOAD_FOLDER ='images'

@app.route('/')
@app.route('/home')
def home():
    posts=Posts.query.all()
    return render_template('home.html', title='Home', posts=posts)
@app.route('/about')
def about():
    return render_template('about.html', title='About')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/post', methods=['GET','POST'])
@login_required
def post():
    form = PostForm()
    if form.validate_on_submit():
        postData = Posts(
        title=form.title.data,
        content=form.content.data,
        author=current_user
    )
                
        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        print(form.errors)
    return render_template('post.html', title='Post', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():

        f = form.image.data
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"images/{f.filename}", BUCKET)

        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = Users(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=hashed_pw,
                url=f"https://ifebucket1234.s3.eu-west-2.amazonaws.com/images/{f.filename}")
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('post'))
    return render_template('register.html', title='Register', form=form)

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        upload_file(f"images/{f.filename}", BUCKET)

        return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)

@app.route("/storage")
def storage():
    contents = list_files("ifebucket1234")
    return render_template('storage.html', contents=contents)

