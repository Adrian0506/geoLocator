import firebase_admin
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from firebase_admin import credentials
from routes.mapRoutes.updatePlots import router as updatePlot_router
from routes.mapRoutes.deletePlots import router as deletePlot_router
from routes.friendRoutes.addFriend import router as addFriend_router
from routes.friendRoutes.getFriends import router as getFriends_router
from routes.loginRoutes.createUser import router as createUser_router
from routes.loginRoutes.loginUser import router as loginUser_router
from routes.refreshToken.refreshToken import router as refreshUser_router

cred = credentials.Certificate('./firebase-key.json') # replace with your actual credentials file path
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://geolocation-8196e-default-rtdb.firebaseio.com/' # replace with your actual Firebase project ID
})

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

# refreshes user if they have a valid token so they do not need to login again
app.include_router(refreshUser_router)

#update plot routers
app.include_router(updatePlot_router)
app.include_router(deletePlot_router)

#user creating
app.include_router(createUser_router)
app.include_router(loginUser_router)

#friend routes
app.include_router(deletePlot_router)
app.include_router(addFriend_router)
app.include_router(getFriends_router)
