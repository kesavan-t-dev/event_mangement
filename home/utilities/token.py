import jwt
import datetime
from django.conf import settings

def generate_jwt_token(account, account_type):
    uid = str(account.user_id) if account_type == "user" else str(account.organiser_id)
    now = datetime.datetime.utcnow()
    
    access_payload = {
        'user_id': uid,
        'type': account_type,
        'iat': now,
    }
    
    refresh_payload = {
        'user_id': uid,
        'type': account_type,
        'exp': now + datetime.timedelta(days=7),
        'iat': now,
    }
    
    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm='HS256')
    
    return access_token, refresh_token



