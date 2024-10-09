from flask import Blueprint, current_app
import click
#from projects.service_layer.users import handlers
#from projects.domain.user import User
#from projects.service_layer.users import unit_of_work

from projects.domain import commands
from projects import views 

bp = Blueprint('auth', __name__)

@bp.cli.command('create-manager')
@click.option('--username')
@click.option('--email')
@click.option('--password')
def create(username, email, password):

    user = None

    #if handlers.get_user_by_username(username, uow):
    #    current_app.logger.info(f"user exists with username: {username}. Please select another username.")
    #    return

    #if handlers.get_user_by_email(email, uow):
    #    current_app.logger.info(f"user exists with e-mail: {email}. Please select another e-mail.")
    #    return

    if not user:
        current_app.users_bus.handle(commands.CreateUser(username, email, password))
        current_app.users_bus.handle(commands.PromoteToManager(username))
        current_app.users_bus.handle(commands.CreateToken(username))
        token = views.token_by_username(username, current_app.users_bus.uow)
        if token:
            current_app.logger.info(f"Manager created with token {token[0]}")
        else:
            current_app.logger.error(f"Failed to create manager user using username: {username}")

from projects.entrypoints.flask.auth import routes
