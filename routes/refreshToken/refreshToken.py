from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing.emailHash import hashEmail
from typing_extensions import Annotated
from firebase_admin import db
from datetime import timedelta
from createToken.createJWTToken import verify_token
from createToken.createJWTToken import create_access_token, create_refresh_token
ACCESS_TOKEN_EXPIRE_MINUTES = 30
access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
@router.get('/refresh/login/{email}')
async def root(email:str, token: Annotated[str, Depends(oauth2_scheme)]):
    if verify_token(token):
        encoded_email = hashEmail(email)
        users_ref = db.reference('/users/' + encoded_email).get()
        print('NEW TOKEN CREATED' + token)

        return {
            "access_token": create_access_token(
            data={"sub": users_ref['firstName']}, expires_delta=access_token_expires
        ),
            "refresh_token": create_refresh_token(email),
            "firstName": users_ref['firstName'],
            "lastName": users_ref['lastName'],
            "mapPoints": users_ref['mapPoints']
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid token")