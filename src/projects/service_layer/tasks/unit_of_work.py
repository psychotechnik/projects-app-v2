# pylint: disable=attribute-defined-outside-init
from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from typing import Callable
#from projects.service_layer import messagebus

from projects import config
from projects.adapters.users import repository


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.Config().SQLALCHEMY_DATABASE_URI,
        isolation_level="SERIALIZABLE",
    )
)

SessionFactory = Callable[[], Session]


class AbstractUnitOfWork(abc.ABC):
    #bus: messagebus.MessageBus
    repo: repository.AbstractRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError



class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory: SessionFactory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = repository.SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
