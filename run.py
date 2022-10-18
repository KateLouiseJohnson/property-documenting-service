from typing import List
from fastapi import Form, File, UploadFile, FastAPI
from models import Property
from database import setup_database, get_connection, insert_property
import json

setup_database()
# TODO: There's definitely something better that could be done with connecting to the 
# DB here, I'm unsure how this works if the connection is lost/interrupted, whether it
# is better to create a connection for each write, although that seems like it would 
# negatively affect performance. I would need to look into this a lot deeper. 
database=get_connection()
app = FastAPI()
# TODO: One obvious piece that is missing is some form of authentication, I figured 
# it was best to try get the basics running before starting to look into this further.

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

    # TODO: This method is starting to grow significantly, it would be ideal to move
    # this functionality out to separate methods, such as controllers and services.
    # I'm also unsure of the best practices when it comes to Python in this regard, 
    # given more time I would look into how best to go about breaking this into 
    # smaller pieces.
    try:
        id = insert_property(database, database.cursor(), property)
        # TODO: The intention at this stage would be to use the property ID to create
        # an entry in a second db table linking this ID to a file path.
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