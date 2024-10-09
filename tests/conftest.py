import os
from dotenv import load_dotenv
import time

import pytest
from sqlalchemy.orm import scoped_session

from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from projects.adapters.users.orm import start_mappers as users_mappers
from projects.adapters.projects.orm import start_mappers as projects_mappers

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv-tests'))


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://eqb:eqb@127.0.0.1:5432/test_projects-app'


def wait_for_pg_to_come_up(engine):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return engine.connect()
        except OperationalError:
            time.sleep(0.5)
    pytest.fail("Postgres never came up")


@pytest.fixture(scope="session")
def db():
    db_uri = TestConfig().SQLALCHEMY_DATABASE_URI
    
    engine = create_engine(db_uri)
    wait_for_pg_to_come_up(engine)
    users_mappers()
    projects_mappers()

    return engine


@pytest.fixture(autouse=True)
def enable_transactional_tests(db):
    '''https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites'''
    connection = db.engine.connect()
    transaction = connection.begin()

    db.session = scoped_session(
        session_factory=sessionmaker(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
    )
    
    yield

    #clear_mappers()
    db.session.close()
    transaction.rollback()
    connection.close()
