from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Disable CSRF checks for API session authentication.
    Safe for internal POS systems.
    """
    def enforce_csrf(self, request):
        return