from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from projects.service_layer.users import handlers
from projects.entrypoints.flask.api.errors import error_response

from projects.service_layer.users import unit_of_work

basic_auth = HTTPBasicAuth()


class MyHTTPTokenAuth(HTTPTokenAuth):

    def authorize(self, role, user, auth):
        if role is None:
            return True
        if isinstance(role, (list, tuple)):
            roles = role
        else:
            roles = [role]
        if user is True:
            user = auth
        if self.get_user_roles_callback is None:  # pragma: no cover
            raise ValueError('get_user_roles callback is not defined')
        user_roles = self.ensure_sync(self.get_user_roles_callback)(auth.token)
        if user_roles is None:
            user_roles = {}
        elif not isinstance(user_roles, (list, tuple)):
            user_roles = {user_roles}
        else:
            user_roles = set(user_roles)
        for role in roles:
            if isinstance(role, (list, tuple)):
                role = set(role)
                if role & user_roles == role:
                    return True
            elif role in user_roles:
                return True

token_auth = MyHTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    return handlers.\
        verify_password(username, password, unit_of_work.SqlAlchemyUnitOfWork())

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token):
    return handlers.\
        check_token(token, unit_of_work.SqlAlchemyUnitOfWork()) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

@token_auth.get_user_roles
def get_user_roles(username):
    return handlers.\
        get_roles(username, unit_of_work.SqlAlchemyUnitOfWork())
