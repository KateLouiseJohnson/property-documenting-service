from fastapi import FastAPI
from models import Property
from database import setup_database, get_connection, insert_property

setup_database()
database=get_connection()
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
    # deal with image and pdf files
    status=''
    message=''
    
    try:
        id = insert_property(database, database.cursor(), property)
        message= 'ID: ' + id
        status='success'
    except Exception as error:
        error=f"{type(error).__name__}: {error}"
        print(error)
        message=error
        status='failure'

    return {
        'status': status,
        'message': message
    }