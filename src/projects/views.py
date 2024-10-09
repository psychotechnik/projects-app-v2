from projects.service_layer.users import unit_of_work
from sqlalchemy.sql import text

def token_by_username(username: str, uow: unit_of_work.SqlAlchemyUnitOfWork) -> str | None:
    with uow:
        results = list(uow.session.execute(
            text('SELECT token FROM users WHERE username = :username'),
            dict(username=username)
        ))
        if results:
            return results[0]
