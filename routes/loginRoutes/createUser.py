from fastapi import APIRouter
from pydantic import BaseModel
from fastapi import HTTPException
from firebase_admin import db
from hashing.passwordHash import get_hashed_password
from hashing.emailHash import hashEmail
from fastapi import APIRouter
from fastapi import HTTPException
from hashing.emailHash import hashEmail
from firebase_admin import db

router = APIRouter()

class NewUser(BaseModel):
    firstName: str
    lastName: str 
    email: str
    password: str

@router.post('/create-user')
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

    user_data = {
        'firstName': firstName,
        'lastName': lastName,
        'email': encoded_email,
        'password': password,
        'friends': ['None'],
        'outGoingRequests': ['None'],
        'mapPoints': [{'lat': '1', 'lng': '1', 'id': 1}],
        'friendRequest': ['None'],
    }

    users_ref.set(user_data)

    raise HTTPException(status_code=200, detail="Created")