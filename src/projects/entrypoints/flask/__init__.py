import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_swagger_ui import get_swaggerui_blueprint

from projects.config import Config

from projects.bootstrap import bootstrap_users, bootstrap_projects


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #from projects.adapters.users import orm as users_orm
    #from projects.adapters.projects import orm as projects_orm
    #from projects.adapters.tasks import orm as tasks_orm

    #users_orm.start_mappers()
    #projects_orm.start_mappers()
    #tasks_orm.start_mappers()

    with app.app_context():
        #db.create_all()
    
        spec = APISpec(
            title="User API",
            version="1.0.0",
            openapi_version="3.0.3",
            plugins=[FlaskPlugin(), MarshmallowPlugin()],
        )   
        
        spec.components.security_scheme(
            "bearerAuth",
            {
                "type": "http",
                # "scheme": "bearer",
                "bearerFormat": "JWT",  
            }
        )
              
        spec.tag({
        'name': 'Authentication',
        'description': 'Operations related to user authentication',
        'x-order': 1
        })

        spec.tag({
            'name': 'User',
            'description': 'Operations related to user management',
            'x-order': 2
        })
        
        spec.tag({
        'name': 'Project',
        'description': 'Operations related to project management',
        'x-order': 3
        })

        spec.tag({
            'name': 'Task',
            'description': 'Operations related to task management in a project',
            'x-order': 4
        })
            
            
        app.spec = spec 

        from projects.entrypoints.flask.api import users, tokens, projects, tasks

        from projects.entrypoints.flask.errors import bp as errors_bp
        app.register_blueprint(errors_bp)

        from projects.entrypoints.flask.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from projects.entrypoints.flask.main import bp as main_bp
        app.register_blueprint(main_bp)

        from projects.entrypoints.flask.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        
        # Registration of routes and specifications
        #from projects.entrypoints.flask.api.tokens import register_routes_and_specs
        #register_routes_and_specs(app)
        
        #from projects.entrypoints.flask.api.users import register_routes_and_specs
        #register_routes_and_specs(app)
        
        #from projects.entrypoints.flask.api.projects import register_routes_and_specs
        #register_routes_and_specs(app)
        
        #from projects.entrypoints.flask.api.tasks import register_routes_and_specs
        #register_routes_and_specs(app)

        app.spec.path(view=users.get_user)
        app.spec.path(view=users.user_by_username)
        app.spec.path(view=users.get_users)
        app.spec.path(view=users.promote_to_manager)
        app.spec.path(view=users.create_user)
        app.spec.path(view=users.delete_user)

        app.spec.path(view=tokens.create_token)
        app.spec.path(view=tokens.revoke_token)
        
        app.spec.path(view=projects.list_projects)
        app.spec.path(view=projects.get_project)
        app.spec.path(view=projects.create_project)
        app.spec.path(view=projects.update_project)
        app.spec.path(view=projects.delete_project)

        app.spec.path(view=tasks.get_tasks)
        app.spec.path(view=tasks.create_task)
        app.spec.path(view=tasks.update_task_status)

        app.users_bus = bootstrap_users()
        app.projects_bus = bootstrap_projects()
        

        # Route to return the specification in JSON format
        @app.route("/static/swagger.json")
        def swagger_json():
            return app.spec.to_dict()  # API specification
        
        #  Swagger UI
        SWAGGER_URL = '/swagger'
        API_URL = '/static/swagger.json'
        swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
        app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) 

        if not app.debug and not app.testing:

            if app.config['LOG_TO_STDOUT']:
                stream_handler = logging.StreamHandler()
                stream_handler.setLevel(logging.INFO)
                app.logger.addHandler(stream_handler)
            else:
                if not os.path.exists('logs'):
                    os.mkdir('logs')
                file_handler = RotatingFileHandler('logs/projects.log',
                                                   maxBytes=10240, backupCount=10)
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s %(levelname)s: %(message)s '
                    '[in %(pathname)s:%(lineno)d]'))
                file_handler.setLevel(logging.INFO)
                app.logger.addHandler(file_handler)

            app.logger.setLevel(logging.INFO)
            app.logger.info('Projects App startup')

    return app


