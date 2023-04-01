from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, db
import base64

cred = credentials.Certificate('./firebase-key.json') # replace with your actual credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://geolocation-8196e-default-rtdb.firebaseio.com/' # replace with your actual Firebase project ID
})

class NewUser(BaseModel):
    firstName: str
    lastName: str 
    email: str
    password: str

class ExistingUser(BaseModel):
    email: str
    password: str

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
    encoded_email = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    users_ref = db.reference('/users/' + encoded_email).get()
    if users_ref is None:
        raise HTTPException(status_code=409, detail="Invalid username or password")
    if users_ref['password'] != password:
        raise HTTPException(status_code=404, detail="Invalid username or password")
    raise HTTPException(status_code=200, detail="Granted")


@app.post('/create-user')
async def root(newUser: NewUser):
    firstName = newUser.firstName
    lastName = newUser.lastName
    email = newUser.email
    password = newUser.password # encode the email address
    encoded_email = base64.b64encode(email.encode('utf-8')).decode('utf-8')
    # users_ref = db.reference('/users/' + encoded_email)
    users_ref = db.reference('/users/' + encoded_email)
    getUsers = users_ref.get()

    if getUsers is not None:
        raise HTTPException(status_code=409, detail="Email exists")

    users_ref.set({
        'firstName': firstName,
        'lastName': lastName,
        'email': encoded_email,
        'password': password
    })

    raise HTTPException(status_code=200, detail="Created")