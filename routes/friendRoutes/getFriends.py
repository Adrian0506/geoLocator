from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing.emailHash import hashEmail
from typing_extensions import Annotated
from firebase_admin import db
from createToken.createJWTToken import verify_token
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get('/get/friends/{email}')
async def root(email:str, token: Annotated[str, Depends(oauth2_scheme)]):
    if verify_token(token):
        encoded_email = hashEmail(email['email'])
        users_ref = db.reference('/users/' + encoded_email)
        get_user_friend = users_ref.get()['friends']
        return get_user_friend
    else:
        raise HTTPException(status_code=401, detail="Invalid token")