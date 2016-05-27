from flask import render_template, request, redirect, flash, make_response
from app import app, forms, db, models, login_manager
from app.uploader import Uploader
from flask.ext.login import current_user, login_required, login_user, logout_user
import hashlib
import datetime
import os
import json
import re

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/upload/', methods=['GET', 'POST', 'OPTIONS'])
def upload():
    """UEditor文件上传接口
    config 配置文件
    result 返回结果
    """
    result = {}
    action = request.args.get('action')

    # 解析JSON格式的配置文件
    with open(os.path.join(app.static_folder, 'ueditor', 'php',
                           'config.json')) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r'\/\*.*\*\/', '', fp.read()))
        except:
            CONFIG = {}

    if action == 'config':
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
        # 图片、文件、视频上传
        if action == 'uploadimage':
            fieldName = CONFIG.get('imageFieldName')
            config = {
                "pathFormat": CONFIG['imagePathFormat'],
                "maxSize": CONFIG['imageMaxSize'],
                "allowFiles": CONFIG['imageAllowFiles']
            }
        elif action == 'uploadvideo':
            fieldName = CONFIG.get('videoFieldName')
            config = {
                "pathFormat": CONFIG['videoPathFormat'],
                "maxSize": CONFIG['videoMaxSize'],
                "allowFiles": CONFIG['videoAllowFiles']
            }
        else:
            fieldName = CONFIG.get('fileFieldName')
            config = {
                "pathFormat": CONFIG['filePathFormat'],
                "maxSize": CONFIG['fileMaxSize'],
                "allowFiles": CONFIG['fileAllowFiles']
            }

        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('uploadscrawl'):
        # 涂鸦上传
        fieldName = CONFIG.get('scrawlFieldName')
        config = {
            "pathFormat": CONFIG.get('scrawlPathFormat'),
            "maxSize": CONFIG.get('scrawlMaxSize'),
            "allowFiles": CONFIG.get('scrawlAllowFiles'),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, 'base64')
            result = uploader.getFileInfo()
        else:
            result['state'] = '上传接口出错'

    elif action in ('catchimage'):
        config = {
            "pathFormat": CONFIG['catcherPathFormat'],
            "maxSize": CONFIG['catcherMaxSize'],
            "allowFiles": CONFIG['catcherAllowFiles'],
            "oriName": "remote.png"
        }
        fieldName = CONFIG['catcherFieldName']

        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif '%s[]' % fieldName in request.form:
            # 而是这个
            source = request.form.getlist('%s[]' % fieldName)

        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, 'remote')
            info = uploader.getFileInfo()
            _list.append({
                'state': info['state'],
                'url': info['url'],
                'original': info['original'],
                'source': imgurl,
            })

        result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
        result['list'] = _list

    else:
        result['state'] = '请求地址出错'

    result = json.dumps(result)

    if 'callback' in request.args:
        callback = request.args.get('callback')
        if re.match(r'^[\w_]+$', callback):
            return '%s(%s)' % (callback, result)
        return json.dumps({'state': 'callback参数不合法'})

    res = make_response(result)
    res.headers['Access-Control-Allow-Origin'] = '*'
    res.headers['Access-Control-Allow-Headers'] = 'X-Requested-With,X_Requested_With'
    return res


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

@app.route('/manage')
@login_required
def manage():
    titleArgs = request.args.get('title')
    typeArgs = request.args.get('type')
    data = None
    if titleArgs is None and typeArgs is None:
        data = models.Post.query.all()
    elif titleArgs is None:
        data = models.Post.query.filter_by(type=typeArgs).all()
    elif typeArgs is None:
        data = models.Post.query.filter_by(title=titleArgs).all()
    else:
        data = models.Post.query.filter_by(type=typeArgs, title=titleArgs).all()
    render_template("manage.html", data=data)
    #TODO: do manage.html

@app.route('/modify/<int:postid>', methods=['GET', 'POST'])
@login_required
def modify(postid):
    post = models.Post.query.filter_by(postid=postid).first()
    if post is None:
        flash("Can't find Post with ID " + str(postid))
        redirect("manage")
    render_template("modify.html", title=post.title, content=post.content, type=post.type)
    #TODO: do modify.html

@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    form = forms.PostForm(request.form)
    if request.method == 'GET':
        return render_template('create.html', form = form)
    if form.validate():
        post = models.Post(userid=current_user.id, content=form.content.data, title=form.title.data, type=form.type.data, createdTime=datetime.datetime.now(), modifiedTime=datetime.datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect('index')
    else:
        return render_template('create.html', form=form)


@app.route('/read/<int:id>')
def read(id):
    data = models.Post.query.filter_by(postid=id).first()
    if data is None:
        flash("Sorry, Invalid rename & modify some htmURL")
        return redirect('index')
    return render_template('read.html', data=data)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/people')
def people():
    return render_template("people.html")


@app.route('/paper')
def paper():
    return render_template("paper.html")


@app.route('/project')
def project():
    return render_template("project.html")


@app.route('/software')
def software():
    return render_template("software.html")


@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/sponsor')
def sponsor():
    return render_template("sponsor.html")


@app.route('/event')
def event():
    return render_template("event.html")


@app.route('/news')
def news():
    return render_template("news.html")







