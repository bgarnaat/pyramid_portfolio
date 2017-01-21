import os
from pyramid.authentication import AuthTkTAuthentication
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import Allow, Authenticated
from pyramid.session import SignedCookieSessionFactory
from passlib.apps import custom_app_context as pwd_context


class NewRoot(object):
    def __init__(self, request):
        self.request = request

    __acl__ = [
        (Allow, Authenticated, 'admin')
    ]


def check_credentials(username, password):
    """Verify username and password."""
    if username and password:
        if username == os.environ.get('AUTH_USERNAME'):
            return pwd_context.verify(password, 'AUTH_PASSWORD')
    return False
