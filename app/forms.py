from app import app
from wtforms import Form, BooleanField, StringField, PasswordField, SelectField
from wtforms import validators, ValidationError

def usernameCheck(form, field):
    valid = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    for i in field.data:
        if i not in valid:
            raise ValidationError("valid username just include digits & letters")

def getChoice():
    a = []
    a.append(('about', 'About'))
    a.append(('event', 'Event'))
    a.append(('news', 'News'))
    a.append(('blog', 'Blog'))
    a.append(('paper', 'Paper'))
    a.append(('project', 'Project'))
    a.append(('software', 'Software'))
    a.append(('sponsor', 'Sponsor'))
    return a;

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
    type = SelectField('Type', [validators.DataRequired(message='Please select the Type')], choices=getChoice())
