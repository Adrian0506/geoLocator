from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing.emailHash import hashEmail, disolveHash
from typing_extensions import Annotated
from firebase_admin import credentials, db
from createToken.createJWTToken import verify_token
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.patch('/update/map/plots')
async def root(payload: dict, token: Annotated[str, Depends(oauth2_scheme)]):
    if verify_token(token):
        encoded_email = hashEmail(payload['email'])
        users_ref = db.reference('/users/' + encoded_email)
        get_user_points = users_ref.get()['mapPoints']

        user_point = {
            'mapPoints': get_user_points,
        }

        currentIndex = 1
        if (len(get_user_points) >= 1):
            currentIndex = get_user_points[-1]['id'] + 1
        user_point['mapPoints'].append({'lat': payload['lat'], 'lng': payload['lng'], 'visitingReason': payload['visitingReason'], 'description': payload['description'], 'id': currentIndex})
        users_ref.update(user_point)
        get_user_points = users_ref.get()['mapPoints']

        return get_user_points
    else:
        raise HTTPException(status_code=401, detail="Invalid token")
