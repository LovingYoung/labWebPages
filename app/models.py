from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.CHAR(40), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    people = db.relationship('People', backref='author', lazy='dynamic')
    papers = db.relationship('Paper', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User %r>" % (self.username)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Post(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    postid = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.TEXT)
    createdTime = db.Column(db.DateTime)
    modifiedTime = db.Column(db.DateTime)
    type = db.Column(db.String(128))
    title = db.Column(db.String(128))

    def __repr__(self):
        return "<PostID: %r>, " % (self.postid)

class People(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    peopleid = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    position = db.Column(db.String(64))
    personalpage = db.Column(db.String(256))
    email = db.Column(db.String(64))
    createdTime = db.Column(db.DateTime)
    modifiedTime = db.Column(db.DateTime)
    photo = db.Column(db.String(256))

class Project(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    projectid = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(512))
    body = db.Column(db.TEXT)
    photo = db.Column(db.String(256))
    createdTime = db.Column(db.DateTime)
    modifiedTime = db.Column(db.DateTime)

class Paper(db.Model):
     userid = db.Column(db.Integer, db.ForeignKey('user.id'))
     paperid = db.Column(db.Integer, primary_key=True, nullable=False)
     name = db.Column(db.String(512))
     pdf = db.Column(db.String(256))
     abstract = db.Column(db.TEXT)
     publishTime = db.Column(db.DateTime)
     createdTime = db.Column(db.DateTime)
     modifiedTime = db.Column(db.DateTime)
