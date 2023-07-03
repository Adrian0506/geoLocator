import os

os.environ['JWT_SECRET_KEY'] = 'secretKey'
os.environ['JWT_REFRESH_SECRET_KEY'] = 'testKey'

print(os.environ)