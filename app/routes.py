from app import app
from .forms import SearchForm
from flask import render_template, session
import os
from flask import request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from .models import Book
from app import db
from flask_mail import Message
from . import celery, mail
from .find_book import FindBook
import time



ALLOWED_EXTENSIONS = set(['pdf'])


@celery.task
def send_async_email(data, email):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        not_found = False
        find_book = FindBook(data)
        start_time = time.time()
        result = find_book.search_books()
        end_time = time.time() - start_time
        app.logger.info('time to find is {:.2} seconds'.format(end_time))
        if not result:
            not_found = True
        msg = Message("You've requested search for '%s'" % data,
                      recipients=[email])
        if not_found:
            msg.html = '<h2>Nothing found on your request :c </h2>'
        else:
            msg.html = render_template('mail.html', result=result)
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        send_async_email.apply_async(args=[form.search.data, form.email.data])
        return redirect(url_for('success'))

    return render_template('search.html', title='Search', form=form)


@app.route('/success')
def success():
    email = session.get('email')
    return render_template('success.html', email=email, title='Success!')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            f = Book(full_path)
            db.session.add(f)
            db.session.commit()
            return redirect(request.url)
    return render_template('upload.html')

