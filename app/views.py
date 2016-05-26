from flask import render_template, request, redirect, flash
from app import app, forms, db, models, login_manager
from flask.ext.login import current_user, login_required, login_user, logout_user
import hashlib

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user is not None and current_user.is_authenticated:
        flash("You have signed in. Please retry after logging out")
        return redirect('index')
    form = forms.LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("Can't find the username")
            return redirect('login')
        if user.password != hashlib.sha1(form.password.data.encode('utf-8')).hexdigest():
            flash("Password Error")
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        flash("Log in success")
        next = request.args.get('next')
        if next is None or next == "":
            return redirect('index')
        else:
            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        find = models.User.query.filter_by(username=form.username.data).first()
        if find is not None:
            flash("The username is not valid.")
            return redirect('register')
        user = models.User(username=form.username.data, password=hashlib.sha1(form.password.data.encode('utf-8')).hexdigest())
        db.session.add(user)
        db.session.commit()
        flash("Register Success.")
        return redirect('login')
    return render_template('register.html', form=form)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('login')

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Log out Success")
    return redirect('index')
