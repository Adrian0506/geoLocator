from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./firebase-key.json') # replace with your actual credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://geolocation-8196e.firebaseio.com' # replace with your actual Firebase project ID
})
db = db.reference()

class NewUser(BaseModel):
    firstName: str
    lastName: str 
    email: str
    password: str

class ExistingUser(BaseModel):
    email: str
    password: str

#geolocation-8196e


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

currentUsers = {}


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/send-user')
async def root(ExistingUser: ExistingUser):
    email = ExistingUser.email
    password = ExistingUser.password
    node_value = db.child('users').get()
    print(node_value)
    if email not in currentUsers:
        raise HTTPException(status_code=404, detail="Invalid username or password")
        return
    print(currentUsers[email]['password'], password)
    if currentUsers[email]['password'] != password:
        raise HTTPException(status_code=404, detail="Invalid username or password")
        return
    raise HTTPException(status_code=200, detail="Granted")
    return {"message": "create"}


@app.post('/create-user')
async def root(newUser: NewUser):
    users_ref = db.reference('users')  
    firstName = newUser.firstName
    lastName = newUser.lastName
    email = newUser.email
    password = newUser.password

    new_user_ref = users_ref.push()
    new_user_ref.set({
        'firstName': firstName,
        'lastName': lastName,
        'password': password,
        'email': email,
    })

    if email in currentUsers:
        raise HTTPException(status_code=404, detail="User already created")
        return
    currentUsers[email] = {
        'firstName': firstName,
        'lastName': lastName,
        'password': password
    }
    raise HTTPException(status_code=200, detail="Created")