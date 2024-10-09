# pylint: disable=bare-except
from __future__ import annotations
import logging
import inspect
from typing import List, Dict, Callable, Type, Union, TYPE_CHECKING
from projects.domain import commands
from projects.service_layer.users import handlers as users_handlers

if TYPE_CHECKING:
    from projects.service_layer.users import unit_of_work as users_unit_of_work
    from projects.service_layer.projects import unit_of_work as projects_unit_of_work

logger = logging.getLogger(__name__)

Message = commands.Command



class MessageBus:

    def __init__(
            self,
            uow: users_unit_of_work.AbstractUnitOfWork | projects_unit_of_work.AbstractUnitOfWork,
    ):
        self.uow = uow
        self.dependencies = dict(uow=uow,)

    def handle(self, message: Message) -> None:
        if isinstance(message, commands.Command):
            self.handle_command(message)
        else:
            raise Exception(f'{message} was not a Command')


    def handle_command(self, 
        command: commands.Command,
        ):
        logger.debug('handling command %s', command)
        try:
            handler = COMMAND_HANDLERS[type(command)]
            self.call_handler_with_dependencies(handler, command)
        except Exception:
            logger.exception('Exception handling command %s', command)
            raise


    def call_handler_with_dependencies(self, handler: Callable, message: Message) -> None:
        params = inspect.signature(handler).parameters
        deps = {
            name: dependency for name, dependency in self.dependencies.items()
            if name in params
        }
        handler(message, **deps)


COMMAND_HANDLERS = {
    commands.CreateUser: users_handlers.create,
    commands.PromoteToManager: users_handlers.promote_to_manager,
    commands.CreateToken: users_handlers.create_token,
    commands.RevokeToken: users_handlers.revoke_token,
}  # type: Dict[Type[commands.Command], Callable]
