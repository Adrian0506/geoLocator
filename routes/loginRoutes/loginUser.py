from pydantic import BaseModel
from fastapi import HTTPException
from datetime import timedelta
from firebase_admin import db
from hashing.passwordHash import verify_password
from hashing.emailHash import hashEmail
from createToken.createJWTToken import create_access_token, create_refresh_token
from fastapi import APIRouter
from fastapi import HTTPException
from hashing.emailHash import hashEmail
from firebase_admin import  db
router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class ExistingUser(BaseModel):
    email: str
    password: str

@router.post('/send-user')
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": create_access_token(
        data={"sub": users_ref['firstName']}, expires_delta=access_token_expires
    ),
        "refresh_token": create_refresh_token(email),
        "firstName": users_ref['firstName'],
        "lastName": users_ref['lastName'],
        "mapPoints": users_ref['mapPoints']
    }
