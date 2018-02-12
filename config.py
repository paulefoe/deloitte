import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'books')
    ALLOWED_EXTENSIONS = set(['pdf'])

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'your_email'
    MAIL_PASSWORD = 'your password'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'me'

