from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField


class SearchForm(FlaskForm):
    search = StringField('Text to search', validators=[DataRequired()])
    email = EmailField('Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Find it!')
