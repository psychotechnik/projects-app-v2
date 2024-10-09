from flask import request, current_app

from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api.errors import bad_request
from projects.entrypoints.flask.schema import UserSchema
from projects.entrypoints.flask.api.errors import error_response 
from projects.service_layer.users import handlers
from projects.service_layer.users import unit_of_work
from projects.domain import commands


@bp.route('/users', methods=['POST'])
@token_auth.login_required(role='manager')
def create_user():
    """
    ---
    post:
      summary: Create a new user
      description: Create a new user account. Only managers are allowed to create users.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - User
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                  description: The desired username.
                email:
                  type: string
                  description: The user's email address.
                password:
                  type: string
                  description: The user's password.
      responses:
        201:
          description: User successfully created.
          content:
            application/json:
              schema: UserSchema
        400:
          description: Invalid input data.
        401:
          description: Unauthorized access.
    """
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')

    #if handlers.get_user_by_username(data['username'], repo):
    #    return bad_request('please use a different username')

    #if handlers.get_user_by_email(data['email'], repo):
    #    return bad_request('please use a different e-mail')

    #handlers.create(
    #        data.get('username'), 
    #        data.get('email'), 
    #        data.get('password'), 
    #        unit_of_work.SqlAlchemyUnitOfWork()
    #)
    cmd = commands.CreateUser(
            data.get('username'), 
            data.get('email'), 
            data.get('password'), 
            )
    current_app.users_bus.handle(cmd)
    return 'OK', 201
  
@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """
    ---
    get:
      summary: Retrieve a user by ID
      description: Retrieve a specific user by their ID.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - User
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the user to retrieve.
      responses:
        200:
          description: Successfully retrieved the user.
          content:
            application/json:
              schema: UserSchema
        401:
          description: Unauthorized access.
        404:
          description: User Not Found.
    """ 
    return handlers.\
        get_user(id, unit_of_work.SqlAlchemyUnitOfWork()) or error_response(404, "User Not Found")
     

@bp.route("/users/user-by-username/<username>", methods=['GET'])
@token_auth.login_required
def user_by_username(username):
    """
    ---
    get:
      summary: Retrieve a user by username
      description: Retrieve a user based on their username.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - User
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username of the user to retrieve.
      responses:
        200:
          description: Successfully retrieved the user.
          content:
            application/json:
              schema:
                type: object
                properties:
                  username:
                    type: string
                  email:
                    type: string
        401:
          description: Unauthorized access.
        404:
          description: User Not Found.
    """  
    return handlers.\
            get_user_by_username(username, unit_of_work.SqlAlchemyUnitOfWork()) or \
        error_response(404, "User Not Found")

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """
    ---
    get:
      summary: Retrieve all users
      description: Get a list of all users.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - User
      responses:
        200:
          description: Successfully retrieved all users.
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    username:
                      type: string
                    email:
                      type: string
        401:
          description: Unauthorized access.
    """    
    return handlers.get_users(unit_of_work.SqlAlchemyUnitOfWork())

@bp.route('/users/promote/<username>', methods=['PATCH'])
@token_auth.login_required(role='manager')
def promote_to_manager(username):
    """
    ---
    patch:
      summary: Promote a user to manager
      description: Grant manager privileges to a specific user.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - User
      parameters:
        - name: username
          in: path
          required: true
          schema:
            type: string
          description: The username of the user to promote.
      responses:
        200:
          description: User successfully promoted.
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: ok
        401:
          description: Unauthorized access.
        404:
          description: User not found.
    """
    if handlers.promote_to_manager(username, unit_of_work.SqlAlchemyUnitOfWork()):
        return {"status": "ok"}, 200
    else:
        error_response(404, "User Not Found")

# Remove user
@bp.route('/user/<int:id>', methods=['DELETE'])
@token_auth.login_required(role='manager')
def delete_user(id):
    """
    ---
    delete:
      summary: Delete a user
      description: Delete a specific user by its ID. Only users with manager role can delete users.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - User
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the user to delete.
      responses:
        204:
          description: User successfully deleted.
        401:
          description: Unauthorized access.
        404:
          description: Not Found.
    """   
    handlers.delete_user(id, unit_of_work.SqlAlchemyUnitOfWork())
    return {"status": "User deleted"}, 204  
      
"""
@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = db.get_or_404(User, id)
    data = request.get_json()
    if 'username' in data and data['username'] != user.username and \
        db.session.scalar(sa.select(User).where(
            User.username == data['username'])):
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
        db.session.scalar(sa.select(User).where(
            User.email == data['email'])):
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return user.to_dict()

"""
