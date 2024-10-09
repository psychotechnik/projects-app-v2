from projects.service_layer.tasks import handlers as task_handlers
from projects.service_layer.projects import handlers as project_handlers
from projects.entrypoints.flask.api.auth import token_auth
from projects.entrypoints.flask.api import bp
from projects.entrypoints.flask.api.errors import bad_request
from flask import jsonify, request
from projects.entrypoints.flask.schema import TaskSchema
from projects.entrypoints.flask.api.errors import error_response
from projects.service_layer.projects import unit_of_work


# Adding a new task to a project
@bp.route('/projects/<int:project_id>/tasks', methods=['POST'])
@token_auth.login_required(role='manager')
def create_task(project_id):
    """ 
    ---
    post:
      summary: Add a new task to a project
      description: Create a new task for a specified project.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - Task
      parameters:
        - in: path
          name: project_id
          required: true
          description: The ID of the project to add a task to.
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                status:
                  type: string
      responses:
        201:
          description: Task successfully created.
          content:
            application/json:
              schema: TaskSchema
        401:
          description: Unauthorized access.
        404:
          description: Project not found.
    """
    data = request.get_json()
    if 'name' not in data :
        return bad_request('must include name')
    project = project_handlers.get_project(project_id, unit_of_work.SqlAlchemyUnitOfWork())
    if project:
      return task_handlers.create_task(
              project_id, 
              data.get("name"),  
              data.get("status"), 
              unit_of_work.SqlAlchemyUnitOfWork()
        ), 201
    return error_response(404, "Project not found")

# Get all tasks for a specific project
@bp.route('/projects/<int:project_id>/tasks', methods=['GET'])
@token_auth.login_required
def get_tasks(project_id):
    """ 
    ---
    get:
      summary: Get all tasks for a project
      description: Retrieve all tasks associated with a specific project.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - Task
      parameters:
        - in: path
          name: project_id
          required: true
          description: The ID of the project to retrieve tasks for.
          schema:
            type: integer
      responses:
        200:
          description: A list of tasks.
          content:
            application/json:
              schema: TaskSchema
        401:
          description: Unauthorized access.
        404:
          description: Task or project not found.
    """
    return task_handlers.get_tasks_for_project(project_id, unit_of_work.SqlAlchemyUnitOfWork()) \
      or error_response(404, "Task or project not found")

# Changing task status
@bp.route('/projects/<int:project_id>/tasks/<int:task_id>', methods=['PUT'])
@token_auth.login_required(role='manager')
def update_task_status(project_id, task_id):
    """ 
    ---
    put:
      summary: Update the status of a task
      description: Change the status of an existing task.
      security:
        - bearerAuth: [] # Using tokens for authentication
      tags:
        - Task
      parameters:
        - in: path
          name: project_id
          required: true
          description: The ID of the project.
          schema:
            type: integer
        - in: path
          name: task_id
          required: true
          description: The ID of the task to update.
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema: 
              type: object
              properties:
                status:
                  type: string
      responses:
        200:
          description: Task status successfully updated.
          content:
            application/json:
              schema: TaskSchema
        401:
          description: Unauthorized access.
        404:
          description: Project not found / Task not found
    """
    data = request.get_json()
    project = project_handlers.get_project(project_id, unit_of_work.SqlAlchemyUnitOfWork())
    if project:
      return task_handlers.update_task_status(project_id, task_id, data.get("status"), unit_of_work.SqlAlchemyUnitOfWork()) \
        or error_response(404, "Task not found")
    return error_response(404, "Project not found")
    
# def register_routes_and_specs(app):
#     with app.app_context(): 
#         app.spec.path(view=get_tasks)
#         app.spec.path(view=create_task)
#         app.spec.path(view=update_task_status)
