from app import app
from wtforms import Form, BooleanField, StringField, PasswordField, SelectField
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
    return a;

def getPosition():
    a = []
    a.append(('director', 'Director'))
    a.append(('faculty', 'Faculty'))
    a.append(('visitingresearcher', 'Visiting Researcher'))
    a.append(('postdoc', 'Postdoc'))
    a.append(('graduatestudent', 'Graduate Student'))
    a.append(('undergraduate', 'Undergraduate'))
    a.append(('staff', 'Staff'))
    a.append(('alumni', 'Alumni'))
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
    content = StringField('Password', [validators.DataRequired(message='Please input content')])
    type = SelectField('Type', [validators.DataRequired(message='Please select the Type')], choices=getPostChoice())

class PeopleForm(Form):
    firstname = StringField('Firstname', [validators.DataRequired(message="Please input First Name"), validators.Length(max=64)])
    lastname= StringField('Lastname', [validators.DataRequired(message="Please input Last Name"), validators.Length(max=64)])
    position = SelectField('Position', [validators.DataRequired(message="Please select Position")], choices=getPosition())
    personalpage = StringField('PersonalPage')
    email = StringField('Email', [validators.Email(message="Please input valid Email"), validators.DataRequired(message="Please input your email")])
    photo = StringField('Photo', [validators.DataRequired('Please select an Photo')])
