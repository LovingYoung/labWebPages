from app import app
from wtforms import Form, BooleanField, StringField, PasswordField, SelectField, FileField, DateField
from wtforms import validators, ValidationError

def usernameCheck(form, field):
    valid = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for i in field.data:
        if i not in valid:
            raise ValidationError("valid username just include digits & letters")

def getPostChoice():
    a = []
    a.append(('about', 'About'))
    a.append(('news', 'News'))
    a.append(('blog', 'Blog'))
    a.append(('paper', 'Paper'))
    a.append(('sponsor', 'Sponsor'))
    return a

def getPosition():
    a = []
    i = 0
    while i < len(app.config['POSITION']):
        a.append((app.config['POSITION'][i], app.config['POSITION_SHOW'][i]))
        i += 1
    return a

class RegisterForm(Form):
    username = StringField('Username', [validators.DataRequired("Please input your username"), validators.Length(min=6, max=16), usernameCheck])
    password = PasswordField('Password', [validators.DataRequired(message="Please input the password"), validators.Length(min=6, max=16)])
    confirm = PasswordField('Confirm', [validators.DataRequired(message="Please input the password again"), validators.equal_to('password', message="You have input two different password")])

    def __repr__(self):
        return "Username:" + self.username.data

class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired("Please input your username"), validators.Length(min=6, max=16), usernameCheck])
    password = PasswordField('Password', [validators.DataRequired(message="Please input the password"), validators.Length(min=6, max=16)])
    remember_me = BooleanField("Remember Me")

    def __repr__(self):
        return "Username:" + self.username.data

class PostForm(Form):
    title = StringField('Username', [validators.DataRequired(message="Please input title"), validators.Length(max=120, message="Please decrease title length to 120 letters or less")])
    content = StringField('Content', [validators.DataRequired(message='Please input content')])
    type = SelectField('Type', [validators.DataRequired(message='Please select the Type')], choices=getPostChoice())

class PeopleForm(Form):
    firstname = StringField('Firstname', [validators.DataRequired(message="Please input First Name"), validators.Length(max=64)])
    lastname= StringField('Lastname', [validators.DataRequired(message="Please input Last Name"), validators.Length(max=64)])
    position = SelectField('Position', [validators.DataRequired(message="Please select Position")], choices=getPosition())
    personalpage = StringField('PersonalPage')
    email = StringField('Email', [validators.Email(message="Please input valid Email"), validators.DataRequired(message="Please input your email")])
    photo = FileField('Photo')

class ProjectForm(Form):
    name = StringField('ProjectName', [validators.DataRequired(message="Please input Project Name"), validators.Length(max=500, message="Please decreate project name to 500 letters or less")])
    body = StringField('ProjectBody', [validators.DataRequired(message="Please input Project body")])
    photo = FileField('Photo')

class PaperForm(Form):
    name = StringField('PaperName', [validators.DataRequired(message="Please input Paper Name"), validators.Length(max=500, message="Please decrease project name to 500 letters or less")])
    abstract = StringField('PaperAbstract', [validators.DataRequired(message="Please input Abstract")])
    publishTime = DateField('PaperPublishTime', [validators.DataRequired(message="Please pick Publish Time")])
    pdf = FileField('PDF')
