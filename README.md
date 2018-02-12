# Deloitte test assignment

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Installing

Create virtualenv


```
git clone https://github.com/svalee/deloitte.git
```

```
cd deloitte
```


Provide all of the necessary settings in files config.py and app/__init__.py

Install requirements
```
pip install -r requirements.txt
```


Start redis server 

```
redis-server
```
Create a Celery worker
```
celery -A app.celery worker
```


Export values
```
export FLASK_APP=deloitte.py
```

Create migration for database

Populate database. The easiest way to do this is to run server, go to /upload/ and upload a few books. Currently supported only pdf extension.

I tried as much as I could to catch all of the exceptions but because formatting standards in PDFs are inconsistent there might be some problems.
Sorry if I missed something, I didn't have enough time to properly test it, add more functionality and make code more readable weekends sure are short.