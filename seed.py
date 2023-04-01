import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('./firebase-key.json') # replace with your actual credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://geolocation-8196e-default-rtdb.firebaseio.com/' # replace with your actual Firebase project ID
})

# create a reference to the users node
users_ref = db.reference('/')

# check if the users node exists, if not, initialize it
users_ref.set({
    'users': {}
})
