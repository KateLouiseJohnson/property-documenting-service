from typing import List
from fastapi import Form, File, UploadFile, FastAPI
from models import Property
from database import setup_database, get_connection, insert_property
import json

setup_database()
# Note: not entirely sure if creating once connection to persist throughout is safe
database=get_connection()
app = FastAPI()
# TODO: Auth!

@app.get('/')
def home():
    return 'Welcome'

@app.get('/ping')
def ping():
    return 'pong'

@app.post('/properties')
def save_property(
    form: str = Form(),
    files: List[UploadFile] = File(...)
):
    status=''
    message=''
    property = Property(**json.loads(form))

    # TODO: create a controller and/or service
    try:
        id = insert_property(database, database.cursor(), property)
        # TODO: handle file storage
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