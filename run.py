from fastapi import FastAPI
from models import Property
from database import setup_database

setup_database()
app = FastAPI()

@app.get('/')
def home():
    return 'Welcome'

@app.get('/ping')
def ping():
    return 'pong'

@app.post('/properties')
def save_property(property: Property):
    # TODO:
    # send data to db
    # deal with image and pdf files
    return {
        'status': 'saving',
        'value': property
    }