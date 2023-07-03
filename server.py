from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
import firebase_admin
from typing_extensions import Annotated
from firebase_admin import credentials, db
from hashing.passwordHash import get_hashed_password, verify_password
from hashing.emailHash import hashEmail, disolveHash
from createToken.createJWTToken import create_access_token, create_refresh_token

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

@app.post('/send-user')
async def root(ExistingUser: ExistingUser):
    email = ExistingUser.email
    password = ExistingUser.password
    encoded_email = hashEmail(email)
    users_ref = db.reference('/users/' + encoded_email).get()
    if users_ref is None:
        raise HTTPException(status_code=409, detail="Invalid username or password")

    passwordVerify = verify_password(password, users_ref['password'])

    if not passwordVerify:
        raise HTTPException(status_code=404, detail="Invalid username or password")

    return {
        "access_token": create_access_token(email),
        "refresh_token": create_refresh_token(email),
        "firstName": users_ref['firstName'],
        "lastName": users_ref['lastName']
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@app.get('/me')
async def root(token: Annotated[str, Depends(oauth2_scheme)]):
    print('test')
    return 'test'

@app.post('/create-user')
async def root(newUser: NewUser):
    firstName = newUser.firstName
    lastName = newUser.lastName
    email = newUser.email
    password = get_hashed_password(newUser.password)
    encoded_email = hashEmail(email)
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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)