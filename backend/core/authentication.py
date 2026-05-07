from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

class JWTCookieAuthentication(JWTAuthentication):
    """
    Custom authentication class that reads the JWT from a cookie.
    """
    def authenticate(self, request):
        # Use settings from SIMPLE_JWT in settings.py or fall back to defaults
        simple_jwt_settings = getattr(settings, 'SIMPLE_JWT', {})
        cookie_name = simple_jwt_settings.get('AUTH_COOKIE', 'access_token')
        
        header = self.get_header(request)
        if header is None:
            raw_token = request.COOKIES.get(cookie_name)
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
            return self.get_user(validated_token), validated_token
        except Exception:
            # Silently fail if token is invalid, allowing other auth classes to try
            return None
