import base64

def hashEmail(email):
    return base64.b64encode(email.encode('utf-8')).decode('utf-8')

def disolveHash(email):
    return base64.b64decode(email).decode('utf-8') 