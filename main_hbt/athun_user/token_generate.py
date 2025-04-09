from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework.response import Response

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def refresh_access_token(refresh_token_str):

    try:
      refresh = RefreshToken(refresh_token_str)
      access = str(refresh.access_token)
      return access
    except TokenError as e: 
      return Response({"error": str(e)}, status=401)    
