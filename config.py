import os


class Config(object):
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    # POSTGRES_URL = os.environ["POSTGRES_URL"]
    # POSTGRES_USER = os.environ["POSTGRES_USER"]
    # POSTGRES_PW = os.environ["POSTGRES_PW"]
    # POSTGRES_DB = os.environ["POSTGRES_DB"]
    # DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
    #                                                                db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = 'postgresql://svalee:cdfhy79k75@localhost/deloitte'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'books')
    ALLOWED_EXTENSIONS = set(['pdf'])

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-Mail configuration

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'triksrimer@gmail.com'
    MAIL_PASSWORD = '2Cfrehf hfcwdtnfkf uhecnysvb ukfpfvb'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = 'me'

