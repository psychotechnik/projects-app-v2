from flask import current_app

from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.auth import basic_auth, token_auth
from projects.service_layer.users import handlers
from projects.service_layer.users import unit_of_work
from projects.domain import commands
from projects import views 


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def create_token():
    """
    ---
    post:
      summary: Create authentication token
      description: Issue a new authentication token for the current user.
      tags:
        - Authentication 
      security:
        - basicAuth: []  # Using Basic Authentication
      responses:
        200:
          description: Token successfully generated.
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                    description: The authentication token.
        401:
          description: Unauthorized. User credentials are invalid.
    """
    username = basic_auth.username()
    current_app.users_bus.handle(commands.CreateToken(username))
    token = views.token_by_username(username, current_app.users_bus.uow)
    return {'token': token}


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required(role='manager')
def revoke_token():
    """
    ---
    delete:
      summary: Revoke authentication token
      description: Revoke the current user's authentication token.
      tags:
        - Authentication
      security:
        - bearerAuth: []  # Using tokens for authentication
      responses:
        204:
          description: Token successfully revoked.
        401:
          description: Unauthorized. User does not have permission or invalid token.
    """
    user = token_auth.current_user()
    current_app.users_bus.handle(commands.RevokeToken(user))
    return '', 204

