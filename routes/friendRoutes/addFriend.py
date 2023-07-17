from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from hashing.emailHash import hashEmail, disolveHash
from typing_extensions import Annotated
from firebase_admin import db
from createToken.createJWTToken import verify_token
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post('/add/friend')
async def root(payload:dict, token: Annotated[str, Depends(oauth2_scheme)]):
    if verify_token(token):
        encoded_email = hashEmail(payload['email'])
        encoded_friend_email = hashEmail(payload['emailToFriend'])
        users_ref = db.reference('/users/' + encoded_email)
        friend_ref = db.reference('/users/' + encoded_friend_email)

        # check if friend exists. We need to do this before calling get or 
        # there will be a error trying to get something that does not exist.
        # so we send a 404 if we can not find a friend to prevent further code execution.
        if friend_ref.get() is None:
            raise HTTPException(status_code=404, detail='Friend not found')
        get_user_friend = users_ref.get()['outGoingRequests']
        get_friend_request = friend_ref.get()['friendRequest']

        # inital value may be None. So we need to account for this
        # if its none lets just populate it with the one friend request otherwise we can
        # append it to array


        #MAKE SURE TO DEHASH EMAIL SO THE USER DOES NOT SEE ODD LOOKING EMAILS
        decoded_email = disolveHash(encoded_email)
        decoded_friend_email = disolveHash(encoded_friend_email)
        if get_friend_request[0] == 'None':
            get_friend_request[0] = decoded_email
        else:
            get_friend_request.append(decoded_email)
        
        if get_user_friend[0] == 'None':
            get_user_friend[0] = decoded_friend_email
        else:
            get_user_friend.append(decoded_friend_email)

        # update the refs and set them and return the payload so we can update it in 
        # our redux state.
        user_request = {
            'friendRequest': get_friend_request,
        }
        friend_request = {
            'outGoingRequests': get_user_friend
        }
        friend_ref.update(user_request)
        users_ref.update(friend_request)
        return get_user_friend
    else:
        raise HTTPException(status_code=401, detail="Invalid token")