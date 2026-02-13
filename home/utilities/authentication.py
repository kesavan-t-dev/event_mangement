import jwt
from django.conf import settings
from ..models import User, Organiser
from rest_framework import status

def verify_token(request):
    from home.services import custom_response
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None, custom_response("Authentication token is missing", status.HTTP_401_UNAUTHORIZED)
    try:
        parts = auth_header.split(' ')
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None, custom_response("Invalid token format. Use 'Bearer <token>'", status.HTTP_401_UNAUTHORIZED)
        
        token = parts[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
    except jwt.ExpiredSignatureError:
        return custom_response("Token has expired", status.HTTP_401_UNAUTHORIZED)
    except jwt.InvalidTokenError:
        return custom_response("Invalid token", status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return custom_response(f"Authentication error: {str(e)}", status.HTTP_401_UNAUTHORIZED)

    user_id = payload.get('user_id')
    account_type = payload.get('type')

    if account_type == "user":
        account = User.objects.filter(pk=user_id).first()
    # else:
    #     account = Organiser.objects.filter(pk=user_id).first()

    if not account:
        return None, custom_response("Account not found", status.HTTP_404_NOT_FOUND)
    account.account_type = account_type
    
    return account, None

    