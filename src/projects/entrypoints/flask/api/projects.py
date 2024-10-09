from projects.service_layer.projects import handlers
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.errors import bad_request
from flask import jsonify, request
from projects.entrypoints.flask.schema import ProjectSchema
from projects.entrypoints.flask.api.errors import error_response
from projects.service_layer.projects import unit_of_work 

# Create new
@bp.route('/projects', methods=['POST'])
@token_auth.login_required(role='manager')
def create_project():
    """
    ---
    post:
      summary: Create a new project
      description: Create a new project. Only users with manager role can create projects.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - Project
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The name of the new project.
                  example: "New Project"
                description:
                  type: string
                  description: A brief description of the project.
                  example: "This is a new project."
      responses:
        201:
          description: Project successfully created.
          content:
            application/json:
              schema: ProjectSchema
        400:
          description: Bad request, missing required fields.
        401:
          description: Unauthorized access.
    """
    data = request.get_json()
    if 'name' not in data :
        return bad_request('must include name')
    return handlers.create_project(
                    data.get('name'), 
                    data.get("description"), 
                    unit_of_work.SqlAlchemyUnitOfWork()
                    ), 201
      
# Getting a specific project by id
@bp.route('/projects/<int:id>', methods=['GET'])
@token_auth.login_required
def get_project(id):
    """
    ---
    get:
      summary: Retrieve a project by ID
      description: Get details of a specific project by its ID.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - Project
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to retrieve.
      responses:
        200:
          description: Successfully retrieved project details.
          content:
            application/json:
              schema: ProjectSchema
        404:
          description: Project not found.
        401:
          description: Unauthorized access.
    """
    return handlers.get_project(id, unit_of_work.SqlAlchemyUnitOfWork()) \
      or error_response(404, "Project not found")

# Get all
@bp.route('/projects', methods=['GET'])
@token_auth.login_required
def list_projects():
    """
    ---
    get:
      summary: Retrieve all projects
      description: Get a list of all projects.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - Project
      responses:
        200:
          description: Successfully retrieved list of projects.
          content:
            application/json:
              schema: ProjectSchema
        404:
          description: There are no projects.      
        401:
          description: Unauthorized access.
    """
    return handlers.list_projects(unit_of_work.SqlAlchemyUnitOfWork()) \
      or error_response(404, "There are no projects")

# Update
@bp.route('/projects/<int:id>', methods=['PUT'])
@token_auth.login_required(role='manager')
def update_project(id):
    """
    ---
    put:
      summary: Update an existing project
      description: Update the details of an existing project by its ID. Only users with manager role can update projects.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - Project
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to update.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  description: The updated name of the project.
                description:
                  type: string
                  description: The updated description of the project.
      responses:
        200:
          description: Project successfully updated.
          content:
            application/json:
              schema: ProjectSchema
        400:
          description: Bad request, missing required fields.
          content:
            application/json:
              schema: ProjectSchema
        401:
          description: Unauthorized access.
        404:
          description: Project not found.
    """    
    data = request.get_json()
    return handlers.update_project(id, data.get("name"), data.get("description"), unit_of_work.SqlAlchemyUnitOfWork()) \
        or error_response(404, "Project not found")
      
# Remove project
@bp.route('/projects/<int:id>', methods=['DELETE'])
@token_auth.login_required(role='manager')
def delete_project(id):
    """
    ---
    delete:
      summary: Delete a project
      description: Delete a specific project by its ID. Only users with manager role can delete projects.
      security:
        - bearerAuth: []  # Using tokens for authentication
      tags:
        - Project
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: The ID of the project to delete.
      responses:
        204:
          description: Project successfully deleted.
        401:
          description: Unauthorized access.
        404:
          description: Project not found.
    """   
    if handlers.delete_project(id, unit_of_work.SqlAlchemyUnitOfWork()):
      return {"status": "Project deleted"}, 204 
    return error_response(404, "Project not found")
      
  
# def register_routes_and_specs(app):
#     with app.app_context(): 
#         app.spec.path(view=list_projects)
#         app.spec.path(view=get_project)
#         app.spec.path(view=create_project)
#         app.spec.path(view=update_project)
#         app.spec.path(view=delete_project)