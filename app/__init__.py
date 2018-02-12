from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from flask_mail import Mail
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery


app = Flask(__name__)

logHandler = RotatingFileHandler('time.log', maxBytes=1000, backupCount=1)

# set the log handler level
logHandler.setLevel(logging.INFO)

# set the app logger level
app.logger.setLevel(logging.INFO)

app.logger.addHandler(logHandler)


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.config.from_object(Config)


mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models