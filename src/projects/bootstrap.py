from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from projects import config
from projects.service_layer import messagebus
from projects.service_layer.users import unit_of_work as users_unit_of_work
from projects.service_layer.projects import unit_of_work as projects_unit_of_work
from projects.adapters.users.orm import start_mappers as users_start_mappers
from projects.adapters.projects.orm import start_mappers as projects_start_mappers

DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.Config().SQLALCHEMY_DATABASE_URI,
        isolation_level="SERIALIZABLE",
    )
)


def bootstrap_users(
        session_factory=DEFAULT_SESSION_FACTORY,
) -> messagebus.MessageBus:
    users_start_mappers()

    uow = users_unit_of_work.SqlAlchemyUnitOfWork(session_factory=session_factory)
    bus = messagebus.MessageBus(uow=uow)
    uow.bus = bus

    return bus

def bootstrap_projects(
        session_factory=DEFAULT_SESSION_FACTORY,
) -> messagebus.MessageBus:
    projects_start_mappers()

    uow = projects_unit_of_work.SqlAlchemyUnitOfWork(session_factory=session_factory)
    bus = messagebus.MessageBus(uow=uow)
    uow.bus = bus

    return bus
