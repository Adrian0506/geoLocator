from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing.emailHash import hashEmail, disolveHash
from typing_extensions import Annotated
from firebase_admin import credentials, db
from createToken.createJWTToken import verify_token
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.delete('/delete/map/plots/{id}/{email}')
async def root(id:int, email: str, token: Annotated[str, Depends(oauth2_scheme)]):
    if verify_token(token):
        encoded_email = hashEmail(email)
        users_ref = db.reference('/users/' + encoded_email)
        get_user_points = users_ref.get()['mapPoints']
        user_point = {
            'mapPoints': get_user_points,
        }
        for index in range(len(user_point['mapPoints'])):
            print(len(user_point))
            if user_point['mapPoints'][index]['id'] == id:
                user_point['mapPoints'].pop(index)
                break
        users_ref.update(user_point)
        get_user_points = users_ref.get()['mapPoints']
        return get_user_points
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
