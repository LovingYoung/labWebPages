from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), index=True, unique=True, nullable=False)
    password = db.Column(db.CHAR(40), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

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
        return "<UserID: %r, "
