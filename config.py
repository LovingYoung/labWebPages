import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY='SNLab'

UPLOAD_FOLDER= os.path.join(basedir, 'app/uploads')
ALLOWED_EXTENSIONS=set(['jpg', 'png','jpeg','JPG','PNG','JPEG'])

POSITION = ['directory', 'faculty', 'visitingresearcher', 'postdoc', 'graduatestudent', 'undergraduate', 'staff', 'alumni']
POSITION_SHOW = ['Directory', 'Faculty', 'Visiting Research', 'Postdoc', 'Graduate Student', 'Undergraduate', 'Staff', 'Alumni']
