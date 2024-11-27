from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Tenta obter o token de acesso do cookie
        raw_token = request.COOKIES.get('access_token')

        if raw_token is None:
            # Não autentica se não houver token
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed:
            return None

        return self.get_user(validated_token), validated_token
